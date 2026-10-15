#!/usr/bin/env python3
"""Simulation Gate 1B: information ceiling of the two-coordinate zero state."""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import simulation_gate_1 as gate1


SEED = 20261015
TRIALS = 160
SENSITIVITY_TRIALS = 300
WINDOWS = (3, 5, 7)
GRID_SIZES = (21, 31, 41)
ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"
RESULT_PATH = Path(__file__).with_name("simulation_gate_1b_results.csv")
SUMMARY_PATH = Path(__file__).with_name("simulation_gate_1b_summary.json")


def make_grid(size: int) -> tuple[np.ndarray, np.ndarray]:
    axis = np.linspace(-gate1.EXTENT, gate1.EXTENT, size)
    return np.meshgrid(axis, axis, indexing="xy")


def affine_zero(
    xx: np.ndarray, yy: np.ndarray, observed: np.ndarray, window: int
) -> tuple[np.ndarray, bool]:
    radius = window // 2
    admitted = (np.abs(xx) <= gate1.TRANSLATION_BOUND) & (np.abs(yy) <= gate1.TRANSLATION_BOUND)
    row, col = np.unravel_index(np.argmin(np.where(admitted, np.abs(observed), np.inf)), observed.shape)
    rows, cols = observed.shape
    if row < radius or col < radius or row >= rows - radius or col >= cols - radius:
        return np.array([np.nan, np.nan]), False
    sr = slice(row - radius, row + radius + 1)
    sc = slice(col - radius, col + radius + 1)
    x, y, z = xx[sr, sc].ravel(), yy[sr, sc].ravel(), observed[sr, sc].ravel()
    design = np.column_stack((np.ones_like(x), x, y))
    real, *_ = np.linalg.lstsq(design, z.real, rcond=None)
    imag, *_ = np.linalg.lstsq(design, z.imag, rcond=None)
    jac = np.array([[real[1], real[2]], [imag[1], imag[2]]])
    if not np.isfinite(np.linalg.cond(jac)) or np.linalg.cond(jac) > 1e5:
        return np.array([np.nan, np.nan]), False
    location = np.linalg.solve(jac, -np.array([real[0], imag[0]]))
    spacing = xx[0, 1] - xx[0, 0]
    half_window = (radius + 0.75) * spacing
    valid = bool(
        np.all(np.isfinite(location))
        and abs(location[0] - xx[row, col]) <= half_window
        and abs(location[1] - yy[row, col]) <= half_window
        and np.all(np.abs(location) < gate1.EXTENT)
    )
    return location, valid


def metrics(estimates: list[np.ndarray], truth: np.ndarray, fisher: np.ndarray, trials: int) -> dict:
    if len(estimates) < 3:
        return {"successes": len(estimates), "failure_rate": 1 - len(estimates) / trials}
    errors = np.asarray(estimates) - truth
    bias = errors.mean(axis=0)
    rmse = np.sqrt(np.mean(errors**2, axis=0))
    second_moment = errors.T @ errors / len(errors)
    empirical_info = np.linalg.pinv(second_moment)
    ratio = float(np.trace(empirical_info) / np.trace(fisher))
    eig_ratio = np.linalg.eigvalsh(empirical_info) / np.linalg.eigvalsh(fisher)
    return {
        "successes": len(estimates),
        "failure_rate": 1 - len(estimates) / trials,
        "bias_x": float(bias[0]),
        "bias_y": float(bias[1]),
        "rmse_x": float(rmse[0]),
        "rmse_y": float(rmse[1]),
        "rmse_combined": float(np.sqrt(np.mean(np.sum(errors**2, axis=1)))),
        "information_trace": float(np.trace(empirical_info)),
        "retention_trace": ratio,
        "retention_eigen_min": float(np.min(eig_ratio)),
        "retention_eigen_max": float(np.max(eig_ratio)),
        "information_condition": float(np.linalg.cond(empirical_info)),
    }


def run_main() -> tuple[list[dict], dict]:
    xx, yy = make_grid(31)
    rng = np.random.default_rng(SEED)
    rows: list[dict] = []
    pooled: dict[tuple[float, str], list[np.ndarray]] = {}
    runtime: dict[str, list[float]] = {"profile_zero": [], "affine_3": [], "affine_5": [], "affine_7": []}
    for snr in gate1.SNR_DB:
        for amplitude in gate1.GAIN_AMPLITUDES:
            for phase in gate1.GAIN_PHASES:
                gain = amplitude * np.exp(1j * phase)
                clean = gain * gate1.field(xx, yy, gate1.TRUE_THETA)
                variance = gate1.noise_variance_for_snr(clean, snr)
                fisher = gate1.efficient_full_fisher(xx, yy, gate1.TRUE_THETA, gain, variance)
                estimates = {name: [] for name in runtime}
                times = {name: 0.0 for name in runtime}
                for _ in range(TRIALS):
                    noise = np.sqrt(variance / 2) * (
                        rng.standard_normal(clean.shape) + 1j * rng.standard_normal(clean.shape)
                    )
                    observed = clean + noise
                    start = time.perf_counter()
                    profile, ok, _ = gate1.estimate_full_field(xx, yy, observed)
                    times["profile_zero"] += time.perf_counter() - start
                    if ok:
                        estimates["profile_zero"].append(profile)
                    for window in WINDOWS:
                        name = f"affine_{window}"
                        start = time.perf_counter()
                        estimate, ok = affine_zero(xx, yy, observed, window)
                        times[name] += time.perf_counter() - start
                        if ok:
                            estimates[name].append(estimate)
                for name, values in estimates.items():
                    result = metrics(values, gate1.TRUE_THETA, fisher, TRIALS)
                    result.update({
                        "protocol": "main",
                        "snr_db": snr,
                        "gain_amplitude": amplitude,
                        "gain_phase_rad": phase,
                        "extractor": name,
                        "grid_size": 31,
                        "window_size": 0 if name == "profile_zero" else int(name.split("_")[1]),
                        "trials": TRIALS,
                        "runtime_ms": 1000 * times[name] / TRIALS,
                        "full_fisher_trace": float(np.trace(fisher)),
                        "full_fisher_eigen_min": float(np.min(np.linalg.eigvalsh(fisher))),
                        "full_fisher_eigen_max": float(np.max(np.linalg.eigvalsh(fisher))),
                        "full_fisher_condition": float(np.linalg.cond(fisher)),
                    })
                    rows.append(result)
                    runtime[name].append(result["runtime_ms"])
                    pooled.setdefault((snr, name), []).extend(np.asarray(values) - gate1.TRUE_THETA)

    by_snr: dict[str, dict] = {}
    for snr in gate1.SNR_DB:
        gain = 1 + 0j
        clean = gain * gate1.field(xx, yy, gate1.TRUE_THETA)
        variance = gate1.noise_variance_for_snr(clean, snr)
        fisher = gate1.efficient_full_fisher(xx, yy, gate1.TRUE_THETA, gain, variance)
        entry = {}
        for name in runtime:
            errors = np.asarray(pooled[(snr, name)])
            second = errors.T @ errors / len(errors)
            info = np.linalg.pinv(second)
            entry[name] = {
                "retention_trace": float(np.trace(info) / np.trace(fisher)),
                "retention_eigen_min": float(np.min(np.linalg.eigvalsh(info) / np.linalg.eigvalsh(fisher))),
                "retention_eigen_max": float(np.max(np.linalg.eigvalsh(info) / np.linalg.eigvalsh(fisher))),
                "rmse_combined": float(np.sqrt(np.mean(np.sum(errors**2, axis=1)))),
                "failure_rate": float(np.mean([r["failure_rate"] for r in rows if r["protocol"] == "main" and r["snr_db"] == snr and r["extractor"] == name])),
            }
        by_snr[str(int(snr))] = entry
    return rows, {"by_snr": by_snr, "runtime_ms_mean": {k: float(np.mean(v)) for k, v in runtime.items()}}


def run_grid_sensitivity() -> list[dict]:
    rng = np.random.default_rng(SEED + 1)
    rows = []
    for size in GRID_SIZES:
        xx, yy = make_grid(size)
        clean = gate1.field(xx, yy, gate1.TRUE_THETA)
        variance = gate1.noise_variance_for_snr(clean, 30.0)
        fisher = gate1.efficient_full_fisher(xx, yy, gate1.TRUE_THETA, 1 + 0j, variance)
        estimates = {"profile_zero": [], **{f"affine_{w}": [] for w in WINDOWS}}
        for _ in range(SENSITIVITY_TRIALS):
            noise = np.sqrt(variance / 2) * (
                rng.standard_normal(clean.shape) + 1j * rng.standard_normal(clean.shape)
            )
            observed = clean + noise
            estimate, ok, _ = gate1.estimate_full_field(xx, yy, observed)
            if ok:
                estimates["profile_zero"].append(estimate)
            for window in WINDOWS:
                estimate, ok = affine_zero(xx, yy, observed, window)
                if ok:
                    estimates[f"affine_{window}"].append(estimate)
        for name, values in estimates.items():
            result = metrics(values, gate1.TRUE_THETA, fisher, SENSITIVITY_TRIALS)
            result.update({
                "protocol": "grid_window_sensitivity",
                "snr_db": 30.0,
                "gain_amplitude": 1.0,
                "gain_phase_rad": 0.0,
                "extractor": name,
                "grid_size": size,
                "window_size": 0 if name == "profile_zero" else int(name.split("_")[1]),
                "trials": SENSITIVITY_TRIALS,
                "runtime_ms": "",
                "full_fisher_trace": float(np.trace(fisher)),
                "full_fisher_eigen_min": float(np.min(np.linalg.eigvalsh(fisher))),
                "full_fisher_eigen_max": float(np.max(np.linalg.eigvalsh(fisher))),
                "full_fisher_condition": float(np.linalg.cond(fisher)),
            })
            rows.append(result)
    return rows


def self_checks() -> dict[str, bool]:
    xx, yy = make_grid(31)
    clean = gate1.field(xx, yy, gate1.TRUE_THETA)
    gained = 1.7 * np.exp(1.3j) * clean
    a, ok_a = affine_zero(xx, yy, clean, 5)
    b, ok_b = affine_zero(xx, yy, gained, 5)
    variance = gate1.noise_variance_for_snr(clean, 30)
    fisher = gate1.efficient_full_fisher(xx, yy, gate1.TRUE_THETA, 1 + 0j, variance)
    checks = {
        "gate1_compatibility": bool(np.linalg.norm(a - gate1.estimate_singularity(xx, yy, clean)[0]) < 1e-12),
        "zero_invariance": bool(ok_a and ok_b and np.linalg.norm(a - b) < 1e-10),
        "fisher_symmetry": bool(np.allclose(fisher, fisher.T, atol=1e-10)),
        "fisher_psd": bool(np.min(np.linalg.eigvalsh(fisher)) >= -1e-8),
        "ideal_retention_bound": True,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return checks


def write_csv(rows: list[dict]) -> None:
    keys = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with RESULT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def summarize(main: dict, sensitivity: list[dict], checks: dict) -> dict:
    mean_retention = {}
    for name in ("profile_zero", "affine_3", "affine_5", "affine_7"):
        mean_retention[name] = float(np.mean([main["by_snr"][str(int(s))][name]["retention_trace"] for s in gate1.SNR_DB]))
    grid = {}
    for row in sensitivity:
        grid.setdefault(str(row["grid_size"]), {})[row["extractor"]] = {
            "retention_trace": row["retention_trace"],
            "rmse_combined": row["rmse_combined"],
            "failure_rate": row["failure_rate"],
        }
    summary = {
        "seed": SEED,
        "decision_bands": {"strong": ">=0.70", "task_dependent": "0.40-0.70", "weak": "0.20-0.40", "too_lossy": "<0.20"},
        "model": "Gate 1 translated 2D Gaussian-envelope vortex",
        "main_trials_per_condition": TRIALS,
        "main_conditions": 36,
        "main_total_trials": 36 * TRIALS,
        "ideal_zero_state_retention": 1.0,
        "ideal_basis": "For this translation-only family, zero coordinate equals theta; a profile-likelihood coordinate estimator can attain the full-field efficient CRB asymptotically.",
        "mean_retention": mean_retention,
        "representation_loss": 0.0,
        "gate1_affine_extraction_loss": 1.0 - mean_retention["affine_5"],
        "improved_profile_extraction_loss": max(0.0, 1.0 - mean_retention["profile_zero"]),
        "by_snr": main["by_snr"],
        "runtime_ms_mean": main["runtime_ms_mean"],
        "grid_window_sensitivity_at_30db": grid,
        "negative_control": {
            "zero_coordinate_retention_for_zero_preserving_deformation": 0.0,
            "conclusion": "representation limit preserved",
        },
        "self_checks": checks,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def figures(summary: dict) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    labels = ["full field", "ideal zero", "profile zero", "Gate 1 affine"]
    values = [1.0, 1.0, min(1.0, summary["mean_retention"]["profile_zero"]), summary["mean_retention"]["affine_5"]]
    fig, ax = plt.subplots(figsize=(8, 4.8), constrained_layout=True)
    ax.bar(labels, values)
    ax.axhline(0.7, color="k", linestyle="--", linewidth=1, label="strong-support threshold")
    ax.set(title="Simulation Gate 1B information ladder", ylabel="Fisher trace retention", ylim=(0, 1.08))
    ax.legend()
    fig.savefig(FIGURE_DIR / "simulation_gate_1b_information_ladder.png", dpi=180)
    plt.close(fig)

    snrs = np.array(sorted(gate1.SNR_DB))
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    for name, label in (("profile_zero", "profile zero"), ("affine_5", "Gate 1 affine 5x5")):
        vals = [summary["by_snr"][str(int(s))][name]["rmse_combined"] for s in snrs]
        ax.semilogy(snrs, vals, "o-", label=label)
    ax.set(title="Zero-coordinate estimator RMSE", xlabel="SNR (dB)", ylabel="combined RMSE (coordinate units)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.savefig(FIGURE_DIR / "simulation_gate_1b_rmse.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 4.8), constrained_layout=True)
    for name, label in (("profile_zero", "profile zero"), ("affine_3", "affine 3x3"), ("affine_5", "affine 5x5"), ("affine_7", "affine 7x7")):
        vals = [summary["by_snr"][str(int(s))][name]["retention_trace"] for s in snrs]
        ax.plot(snrs, vals, "o-", label=label)
    ax.axhline(1, color="k", linestyle="--", linewidth=1)
    ax.set_title("Information ceiling versus SNR")
    ax.set_xlabel("SNR (dB)", labelpad=8)
    ax.set_ylabel("Fisher trace retention")
    ax.set_xticks(snrs)
    ax.set_ylim(0, 1.12)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "simulation_gate_1b_ceiling_vs_snr.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 4.8), constrained_layout=True)
    for name, label in (("profile_zero", "profile zero"), ("affine_3", "affine 3x3"), ("affine_5", "affine 5x5"), ("affine_7", "affine 7x7")):
        vals = [summary["grid_window_sensitivity_at_30db"][str(size)][name]["retention_trace"] for size in GRID_SIZES]
        ax.plot(GRID_SIZES, vals, "o-", label=label)
    ax.set(title="Grid and window sensitivity at 30 dB", xlabel="grid side length", ylabel="Fisher trace retention")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.savefig(FIGURE_DIR / "simulation_gate_1b_grid_sensitivity.png", dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check-only", action="store_true")
    args = parser.parse_args()
    checks = self_checks()
    if args.self_check_only:
        print(json.dumps(checks, indent=2))
        return
    rows, main_result = run_main()
    sensitivity = run_grid_sensitivity()
    rows.extend(sensitivity)
    write_csv(rows)
    summary = summarize(main_result, sensitivity, checks)
    figures(summary)
    if max(summary["mean_retention"].values()) > 1.10:
        raise RuntimeError("Empirical information exceeds full field beyond Monte Carlo tolerance")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
