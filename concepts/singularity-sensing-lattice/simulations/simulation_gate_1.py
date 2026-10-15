#!/usr/bin/env python3
"""Simulation Gate 1: matched-data 2D translation information comparison."""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares


SEED = 20261015
GRID_SIZE = 31
EXTENT = 2.5
ENVELOPE_SIGMA = 1.15
TRUE_THETA = np.array([0.17, -0.13])
SNR_DB = (40.0, 30.0, 20.0, 10.0)
GAIN_AMPLITUDES = (0.7, 1.0, 1.4)
GAIN_PHASES = (0.0, 0.9, 2.1)
TRIALS_PER_CONDITION = 80
LOCAL_RADIUS = 2
MAX_NFEV = 80
TRANSLATION_BOUND = 0.6
ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"
RESULT_PATH = Path(__file__).with_name("simulation_gate_1_results.csv")
SUMMARY_PATH = Path(__file__).with_name("simulation_gate_1_summary.json")


@dataclass
class ConditionResult:
    snr_db: float
    gain_amplitude: float
    gain_phase_rad: float
    trials: int
    full_successes: int
    singularity_successes: int
    full_failure_rate: float
    singularity_failure_rate: float
    full_bias_x: float
    full_bias_y: float
    singularity_bias_x: float
    singularity_bias_y: float
    full_rmse_x: float
    full_rmse_y: float
    full_rmse_combined: float
    singularity_rmse_x: float
    singularity_rmse_y: float
    singularity_rmse_combined: float
    full_runtime_ms: float
    singularity_runtime_ms: float
    full_fisher_trace: float
    singularity_fisher_trace: float
    information_trace_ratio: float
    full_crb_x_std: float
    full_crb_y_std: float


def grid() -> tuple[np.ndarray, np.ndarray, float]:
    axis = np.linspace(-EXTENT, EXTENT, GRID_SIZE)
    xx, yy = np.meshgrid(axis, axis, indexing="xy")
    return xx, yy, float(axis[1] - axis[0])


def field(xx: np.ndarray, yy: np.ndarray, theta: np.ndarray, deformation: float = 0.0) -> np.ndarray:
    """Translated isolated zero with a smooth envelope and optional zero-preserving deformation."""
    u = xx - theta[0]
    v = yy - theta[1]
    r2 = u * u + v * v
    base = (u + 1j * v) * np.exp(-r2 / (2.0 * ENVELOPE_SIGMA**2))
    return base * (1.0 + deformation * r2 / ENVELOPE_SIGMA**2)


def eliminate_gain(template: np.ndarray, observed: np.ndarray) -> complex:
    denom = np.vdot(template, template).real
    return np.vdot(template, observed) / denom


def estimate_full_field(xx: np.ndarray, yy: np.ndarray, observed: np.ndarray) -> tuple[np.ndarray, bool, int]:
    def residual(theta: np.ndarray) -> np.ndarray:
        template = field(xx, yy, theta)
        gain = eliminate_gain(template, observed)
        delta = gain * template - observed
        return np.concatenate((delta.real.ravel(), delta.imag.ravel()))

    admitted = (np.abs(xx) <= TRANSLATION_BOUND) & (np.abs(yy) <= TRANSLATION_BOUND)
    search_metric = np.where(admitted, np.abs(observed), np.inf)
    initial_index = np.unravel_index(np.argmin(search_metric), observed.shape)
    initial = np.array([xx[initial_index], yy[initial_index]])
    fit = least_squares(
        residual,
        initial,
        bounds=([-TRANSLATION_BOUND, -TRANSLATION_BOUND], [TRANSLATION_BOUND, TRANSLATION_BOUND]),
        max_nfev=MAX_NFEV,
        xtol=1e-10,
        ftol=1e-10,
        gtol=1e-10,
    )
    valid = bool(fit.success and np.all(np.isfinite(fit.x)) and np.all(np.abs(fit.x) < TRANSLATION_BOUND))
    return fit.x, valid, int(fit.nfev)


def estimate_singularity(xx: np.ndarray, yy: np.ndarray, observed: np.ndarray) -> tuple[np.ndarray, bool]:
    """Locate a zero by a local affine complex-field least-squares fit."""
    admitted = (np.abs(xx) <= TRANSLATION_BOUND) & (np.abs(yy) <= TRANSLATION_BOUND)
    search_metric = np.where(admitted, np.abs(observed), np.inf)
    row, col = np.unravel_index(np.argmin(search_metric), observed.shape)
    if row < LOCAL_RADIUS or col < LOCAL_RADIUS or row >= GRID_SIZE - LOCAL_RADIUS or col >= GRID_SIZE - LOCAL_RADIUS:
        return np.array([np.nan, np.nan]), False
    sl_r = slice(row - LOCAL_RADIUS, row + LOCAL_RADIUS + 1)
    sl_c = slice(col - LOCAL_RADIUS, col + LOCAL_RADIUS + 1)
    x = xx[sl_r, sl_c].ravel()
    y = yy[sl_r, sl_c].ravel()
    z = observed[sl_r, sl_c].ravel()
    design = np.column_stack((np.ones_like(x), x, y))
    coef_r, *_ = np.linalg.lstsq(design, z.real, rcond=None)
    coef_i, *_ = np.linalg.lstsq(design, z.imag, rcond=None)
    jac = np.array([[coef_r[1], coef_r[2]], [coef_i[1], coef_i[2]]])
    rhs = -np.array([coef_r[0], coef_i[0]])
    if np.linalg.cond(jac) > 1e5:
        return np.array([np.nan, np.nan]), False
    location = np.linalg.solve(jac, rhs)
    half_window = (LOCAL_RADIUS + 0.75) * (xx[0, 1] - xx[0, 0])
    valid = bool(
        np.all(np.isfinite(location))
        and abs(location[0] - xx[row, col]) <= half_window
        and abs(location[1] - yy[row, col]) <= half_window
        and np.all(np.abs(location) < EXTENT)
    )
    return location, valid


def numerical_derivative(xx: np.ndarray, yy: np.ndarray, theta: np.ndarray, index: int, step: float = 1e-6) -> np.ndarray:
    offset = np.zeros(2)
    offset[index] = step
    return (field(xx, yy, theta + offset) - field(xx, yy, theta - offset)) / (2.0 * step)


def efficient_full_fisher(
    xx: np.ndarray, yy: np.ndarray, theta: np.ndarray, gain: complex, noise_variance: float
) -> np.ndarray:
    template = field(xx, yy, theta)
    columns = [
        gain * numerical_derivative(xx, yy, theta, 0),
        gain * numerical_derivative(xx, yy, theta, 1),
        template,
        1j * template,
    ]
    jac = np.column_stack([c.ravel() for c in columns])
    fisher = (2.0 / noise_variance) * np.real(jac.conj().T @ jac)
    theta_block = fisher[:2, :2]
    cross = fisher[:2, 2:]
    nuisance = fisher[2:, 2:]
    efficient = theta_block - cross @ np.linalg.pinv(nuisance) @ cross.T
    return 0.5 * (efficient + efficient.T)


def noise_variance_for_snr(signal: np.ndarray, snr_db: float) -> float:
    mean_signal_power = float(np.mean(np.abs(signal) ** 2))
    return mean_signal_power / (10.0 ** (snr_db / 10.0))


def error_metrics(estimates: list[np.ndarray], theta: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, np.ndarray]:
    errors = np.asarray(estimates) - theta
    bias = np.mean(errors, axis=0)
    rmse_axes = np.sqrt(np.mean(errors**2, axis=0))
    combined = float(np.sqrt(np.mean(np.sum(errors**2, axis=1))))
    covariance = np.cov(errors, rowvar=False, ddof=1)
    return bias, rmse_axes, combined, covariance


def run_condition(
    rng: np.random.Generator,
    xx: np.ndarray,
    yy: np.ndarray,
    snr_db: float,
    amplitude: float,
    phase: float,
) -> ConditionResult:
    gain = amplitude * np.exp(1j * phase)
    clean = gain * field(xx, yy, TRUE_THETA)
    noise_variance = noise_variance_for_snr(clean, snr_db)
    full_estimates: list[np.ndarray] = []
    singularity_estimates: list[np.ndarray] = []
    full_time = 0.0
    singularity_time = 0.0
    for _ in range(TRIALS_PER_CONDITION):
        noise = np.sqrt(noise_variance / 2.0) * (
            rng.standard_normal(clean.shape) + 1j * rng.standard_normal(clean.shape)
        )
        observed = clean + noise
        start = time.perf_counter()
        full_estimate, full_ok, _ = estimate_full_field(xx, yy, observed)
        full_time += time.perf_counter() - start
        start = time.perf_counter()
        singularity_estimate, singularity_ok = estimate_singularity(xx, yy, observed)
        singularity_time += time.perf_counter() - start
        if full_ok:
            full_estimates.append(full_estimate)
        if singularity_ok:
            singularity_estimates.append(singularity_estimate)

    if len(full_estimates) < 3 or len(singularity_estimates) < 3:
        raise RuntimeError("Too few successful estimates for a stable comparison")
    full_bias, full_rmse, full_combined, _ = error_metrics(full_estimates, TRUE_THETA)
    sing_bias, sing_rmse, sing_combined, sing_cov = error_metrics(singularity_estimates, TRUE_THETA)
    full_fisher = efficient_full_fisher(xx, yy, TRUE_THETA, gain, noise_variance)
    singularity_fisher = np.linalg.pinv(sing_cov)
    full_crb = np.sqrt(np.diag(np.linalg.pinv(full_fisher)))
    return ConditionResult(
        snr_db=snr_db,
        gain_amplitude=amplitude,
        gain_phase_rad=phase,
        trials=TRIALS_PER_CONDITION,
        full_successes=len(full_estimates),
        singularity_successes=len(singularity_estimates),
        full_failure_rate=1.0 - len(full_estimates) / TRIALS_PER_CONDITION,
        singularity_failure_rate=1.0 - len(singularity_estimates) / TRIALS_PER_CONDITION,
        full_bias_x=float(full_bias[0]),
        full_bias_y=float(full_bias[1]),
        singularity_bias_x=float(sing_bias[0]),
        singularity_bias_y=float(sing_bias[1]),
        full_rmse_x=float(full_rmse[0]),
        full_rmse_y=float(full_rmse[1]),
        full_rmse_combined=full_combined,
        singularity_rmse_x=float(sing_rmse[0]),
        singularity_rmse_y=float(sing_rmse[1]),
        singularity_rmse_combined=sing_combined,
        full_runtime_ms=1000.0 * full_time / TRIALS_PER_CONDITION,
        singularity_runtime_ms=1000.0 * singularity_time / TRIALS_PER_CONDITION,
        full_fisher_trace=float(np.trace(full_fisher)),
        singularity_fisher_trace=float(np.trace(singularity_fisher)),
        information_trace_ratio=float(np.trace(singularity_fisher) / np.trace(full_fisher)),
        full_crb_x_std=float(full_crb[0]),
        full_crb_y_std=float(full_crb[1]),
    )


def negative_control(xx: np.ndarray, yy: np.ndarray) -> dict[str, float]:
    """Compare information about a zero-preserving radial deformation after eliminating gain."""
    theta = TRUE_THETA
    gain = 1.0 + 0.0j
    clean = gain * field(xx, yy, theta)
    variance = noise_variance_for_snr(clean, 30.0)
    step = 1e-6
    dq = gain * (field(xx, yy, theta, step) - field(xx, yy, theta, -step)) / (2.0 * step)
    template = field(xx, yy, theta)
    jac = np.column_stack((dq.ravel(), template.ravel(), (1j * template).ravel()))
    fisher = (2.0 / variance) * np.real(jac.conj().T @ jac)
    efficient = fisher[0, 0] - fisher[0, 1:] @ np.linalg.pinv(fisher[1:, 1:]) @ fisher[1:, 0]
    zero_a, ok_a = estimate_singularity(xx, yy, field(xx, yy, theta, -0.25))
    zero_b, ok_b = estimate_singularity(xx, yy, field(xx, yy, theta, 0.25))
    return {
        "deformation_minus": -0.25,
        "deformation_plus": 0.25,
        "full_field_efficient_fisher": float(efficient),
        "singularity_coordinate_fisher": 0.0,
        "noiseless_zero_shift": float(np.linalg.norm(zero_b - zero_a)),
        "localizations_valid": bool(ok_a and ok_b),
    }


def self_checks(xx: np.ndarray, yy: np.ndarray) -> dict[str, bool]:
    zero, ok = estimate_singularity(xx, yy, field(xx, yy, TRUE_THETA))
    gained_zero, gained_ok = estimate_singularity(
        xx, yy, (1.7 * np.exp(1.3j)) * field(xx, yy, TRUE_THETA)
    )
    fisher = efficient_full_fisher(
        xx, yy, TRUE_THETA, 1.0 + 0.0j, noise_variance_for_snr(field(xx, yy, TRUE_THETA), 30.0)
    )
    sanity, sanity_ok, _ = estimate_full_field(xx, yy, field(xx, yy, TRUE_THETA))
    checks = {
        "zero_location": bool(ok and np.linalg.norm(zero - TRUE_THETA) < 2e-3),
        "gain_invariance": bool(gained_ok and np.linalg.norm(gained_zero - zero) < 1e-10),
        "fisher_symmetry": bool(np.allclose(fisher, fisher.T, atol=1e-10)),
        "fisher_psd": bool(np.linalg.eigvalsh(fisher).min() >= -1e-8),
        "estimator_sanity": bool(sanity_ok and np.linalg.norm(sanity - TRUE_THETA) < 1e-7),
    }
    if not all(checks.values()):
        raise AssertionError(f"Internal check failure: {checks}")
    return checks


def write_results(results: list[ConditionResult]) -> None:
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(results[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(result) for result in results)


def aggregate(results: list[ConditionResult], checks: dict[str, bool], control: dict[str, float]) -> dict:
    by_snr = {}
    for snr in SNR_DB:
        rows = [r for r in results if r.snr_db == snr]
        by_snr[str(int(snr))] = {
            "full_rmse_combined_mean": float(np.mean([r.full_rmse_combined for r in rows])),
            "singularity_rmse_combined_mean": float(np.mean([r.singularity_rmse_combined for r in rows])),
            "information_trace_ratio_mean": float(np.mean([r.information_trace_ratio for r in rows])),
            "full_failure_rate_mean": float(np.mean([r.full_failure_rate for r in rows])),
            "singularity_failure_rate_mean": float(np.mean([r.singularity_failure_rate for r in rows])),
        }
    summary = {
        "seed": SEED,
        "grid_size": [GRID_SIZE, GRID_SIZE],
        "complex_samples": GRID_SIZE * GRID_SIZE,
        "full_field_real_values": 2 * GRID_SIZE * GRID_SIZE,
        "singularity_state_real_values": 2,
        "compression_ratio": GRID_SIZE * GRID_SIZE,
        "trials_per_condition": TRIALS_PER_CONDITION,
        "conditions": len(results),
        "total_trials": len(results) * TRIALS_PER_CONDITION,
        "snr_definition": "10 log10(mean(|g Psi|^2) / E|n|^2)",
        "noise_definition": "circular complex Gaussian; each real component has variance sigma_n^2/2",
        "by_snr": by_snr,
        "overall": {
            "full_rmse_combined_mean": float(np.mean([r.full_rmse_combined for r in results])),
            "singularity_rmse_combined_mean": float(np.mean([r.singularity_rmse_combined for r in results])),
            "information_trace_ratio_mean": float(np.mean([r.information_trace_ratio for r in results])),
            "information_trace_ratio_min": float(np.min([r.information_trace_ratio for r in results])),
            "information_trace_ratio_max": float(np.max([r.information_trace_ratio for r in results])),
            "full_failure_rate_mean": float(np.mean([r.full_failure_rate for r in results])),
            "singularity_failure_rate_mean": float(np.mean([r.singularity_failure_rate for r in results])),
            "full_runtime_ms_mean": float(np.mean([r.full_runtime_ms for r in results])),
            "singularity_runtime_ms_mean": float(np.mean([r.singularity_runtime_ms for r in results])),
        },
        "negative_control": control,
        "self_checks": checks,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def make_figures(xx: np.ndarray, yy: np.ndarray, results: list[ConditionResult], summary: dict) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    clean = field(xx, yy, TRUE_THETA)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), constrained_layout=True)
    im0 = axes[0].imshow(np.abs(clean), origin="lower", extent=(-EXTENT, EXTENT, -EXTENT, EXTENT))
    axes[0].plot(TRUE_THETA[0], TRUE_THETA[1], "wx", ms=9, mew=2, label="true zero")
    axes[0].set(title="Translated vortex magnitude", xlabel="x", ylabel="y")
    axes[0].legend()
    fig.colorbar(im0, ax=axes[0], label="|Psi|")
    im1 = axes[1].imshow(np.angle(clean), origin="lower", extent=(-EXTENT, EXTENT, -EXTENT, EXTENT), cmap="twilight")
    axes[1].plot(TRUE_THETA[0], TRUE_THETA[1], "kx", ms=9, mew=2)
    axes[1].set(title="Translated vortex phase", xlabel="x", ylabel="y")
    fig.colorbar(im1, ax=axes[1], label="phase (rad)")
    fig.savefig(FIGURE_DIR / "simulation_gate_1_field.png", dpi=180)
    plt.close(fig)

    snrs = np.array(sorted(SNR_DB))
    full = np.array([summary["by_snr"][str(int(s))]["full_rmse_combined_mean"] for s in snrs])
    sing = np.array([summary["by_snr"][str(int(s))]["singularity_rmse_combined_mean"] for s in snrs])
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.semilogy(snrs, full, "o-", label="full-field NLS")
    ax.semilogy(snrs, sing, "s-", label="singularity local fit")
    ax.set(title="Translation error from matched noisy samples", xlabel="SNR (dB)", ylabel="combined RMSE (coordinate units)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.savefig(FIGURE_DIR / "simulation_gate_1_rmse.png", dpi=180)
    plt.close(fig)

    ratios = np.array([summary["by_snr"][str(int(s))]["information_trace_ratio_mean"] for s in snrs])
    fig, ax = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
    ax.plot(snrs, ratios, "o-")
    ax.axhline(1.0, color="k", linestyle="--", linewidth=1, label="full-field bound")
    ax.set_title("Empirical singularity information retention")
    ax.set_xlabel("SNR (dB)", labelpad=8)
    ax.set_ylabel("singularity/full-field Fisher trace ratio")
    ax.set_xticks(snrs)
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "simulation_gate_1_information.png", dpi=180)
    plt.close(fig)

    control = summary["negative_control"]
    fig, ax = plt.subplots(figsize=(6.5, 4.2), constrained_layout=True)
    ax.bar(["full field", "zero coordinate"], [control["full_field_efficient_fisher"], control["singularity_coordinate_fisher"]])
    ax.set(title="Negative control: zero-preserving deformation", ylabel="efficient Fisher information (relative units)")
    fig.savefig(FIGURE_DIR / "simulation_gate_1_negative_control.png", dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check-only", action="store_true")
    args = parser.parse_args()
    xx, yy, _ = grid()
    checks = self_checks(xx, yy)
    if args.self_check_only:
        print(json.dumps(checks, indent=2))
        return
    rng = np.random.default_rng(SEED)
    results = [
        run_condition(rng, xx, yy, snr, amplitude, phase)
        for snr in SNR_DB
        for amplitude in GAIN_AMPLITUDES
        for phase in GAIN_PHASES
    ]
    control = negative_control(xx, yy)
    write_results(results)
    summary = aggregate(results, checks, control)
    make_figures(xx, yy, results, summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
