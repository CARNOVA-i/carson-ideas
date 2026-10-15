# Simulation Gate 2: Multi-Mode Compact State

## 1. Objective

Test whether a low-dimensional singularity-centered state preserves most task-relevant information for a bounded 2D family containing zero-moving and zero-preserving modes.

## 2. Decision Criteria

Criteria were fixed in source before the final run. `PASS` requires a state of at most 20 real values, at least 90% joint generalized efficient information, at least 70% retention for every required parameter, stable estimation across 40, 30, 20, and 10 dB, and a plausible architectural advantage. The alternate joint bands are: excellent at least 95%, strong 90–95%, partial 75–90%, weak 50–75%, and insufficient below 50%.

## 3. Prior Gate Baseline

The exact baseline was `f6106b5e75396646f88eaa9ebd10a31943fcaddc`. Gate 1 remains `HOLD`. Gate 1B remains `PASS` only for its bounded translation information-ceiling question. Gate 2 does not reinterpret either result.

## 4. Multi-Mode Field Model

With `u=x-dx`, `v=y-dy`, and `r2=u^2+v^2`, the field is

`Psi=(u+i v) exp(-((1+alpha)u^2+(1-alpha)v^2)/(2 sigma^2)) exp(i beta r2/sigma^2)`.

The zero remains exactly at `(dx,dy)`. `alpha` changes envelope anisotropy without moving the zero. `beta` adds radial phase curvature without moving the zero. The family is deliberately local, analytic, and not a propagation or hardware model.

## 5. Target Parameters

`theta=[dx,dy,alpha,beta]`. Five bounded points were used: nominal, translated, deformation-dominant, mixed, and a valid conditioned-edge point. The full-field efficient Fisher matrix had rank four at the checked operating point.

## 6. Nuisance Parameters

Unknown nonzero global complex gain was retained. The main run used `g=1.25 exp(0.73 i)`. Full-field Fisher information eliminated its real and imaginary components by Schur complement. Compact descriptors normalized global amplitude and phase.

## 7. Detector and Noise Model

The detector was the prior 31x31 grid over `[-2.5,2.5]^2`: 961 complex or 1,922 real samples. Noise was circular complex Gaussian, with SNR defined from mean clean-field power. The sweep was 40, 30, 20, and 10 dB.

## 8. Full-Field Benchmark

The benchmark used the full local likelihood score for all four targets with complex gain treated as nuisance. Its Fisher matrix was the reference. A local generalized least-squares estimator supplied paired-noise RMSE and timing. This is a competitive local benchmark, not a global large-error recovery test.

## 9. Compact-State Definitions

- `S2_position`, dimension 2: local affine zero coordinates.
- `S6_jacobian`, dimension 6: position plus four normalized Gram/Jacobian geometry quantities.
- `S14_descriptor`, dimension 14: position plus six complex, gain-normalized local polynomial-coefficient ratios through selected cubic terms.
- `P50_patch`, dimension 50: normalized 5x5 complex patch, used as a local upper benchmark.
- Full field, dimension 1,922.

## 10. Gain-Invariant Feature Construction

Jacobian geometry was normalized by its Gram trace. Polynomial coefficients were divided by a local linear complex coefficient with spatial scaling. The patch was norm-normalized and phase-aligned to a deterministic weighted complex anchor. Noiseless checks under gain `1.8 exp(1.1 i)` passed for every compact state.

## 11. Estimators

Compact estimators used local generalized least squares from finite-difference state sensitivities and paired Monte Carlo state covariance. This transparent local-linear method exposes rank loss rather than hiding it behind a learned mapping. It does not prove global convergence outside the admitted local neighborhoods.

## 12. Fisher Information Framework

The full-field target Fisher matrix was reduced over complex gain. Compact Fisher matrices were `J_S^T Cov(S)^+ J_S`. Reported joint trace retention is the mean eigenvalue of the compact Fisher matrix whitened by the full-field Fisher matrix and capped at the data-processing ceiling. Determinant retention is the geometric mean of those four generalized eigenvalues. Per-parameter values compare Fisher diagonal sensitivity and are capped at one.

## 13. Monte Carlo Protocol

Seed `20261015` generated 120 paired trials for each of 20 conditions: five target points by four SNR levels, for 2,400 paired trials. Each noisy field was shared by every representation. Timing fields are excluded from the deterministic digest.

## 14. Mode-by-Mode Information Retention

Mean retention over all conditions:

| State | dx | dy | alpha | beta | Worst |
|---|---:|---:|---:|---:|---:|
| S2 | 11.84% | 11.49% | 0.000019% | 0.000024% | 0.000019% |
| S6 | 12.31% | 11.82% | 0.000556% | 0.000032% | 0.000032% |
| S14 | 17.79% | 17.37% | 0.0233% | 0.0102% | 0.0102% |
| P50 | 17.41% | 13.39% | 0.0031% | 0.0032% | 0.0031% |
| Full field | 100% | 100% | 100% | 100% | 100% |

The zero-preserving modes were effectively absent from every tested local state. Position alone reproduced the intended negative control.

## 15. Joint Information Retention

| State | Dimension | Mean generalized retention | Determinant retention |
|---|---:|---:|---:|
| S2 | 2 | 5.86% | approximately 0% |
| S6 | 6 | 6.07% | 0.0113% |
| S14 | 14 | 8.84% | 0.506% |
| P50 | 50 | 7.70% | 0.191% |
| Full field | 1,922 | 100% | 100% |

No compact state reached even the 50% band. No state met the 70% per-parameter floor.

## 16. State Dimensionality and Compression

Post-extraction dimensionality reductions were 961x for S2, 320.3x for S6, 137.3x for S14, and 38.44x for P50. These are not detector or acquisition compression ratios because every extractor consumed the full sampled field.

## 17. Locality Test

Classification: **C, global field context remains necessary** for this field family and these features. The 5x5 patch retained only 7.70% joint information. Its failure is consistent with `alpha` and `beta` accumulating evidence across radius rather than at the exact zero.

## 18. Computational Cost

Mean implemented local-linear pipeline timing per trial:

| State | Extraction | Estimation | Total |
|---|---:|---:|---:|
| S2 | 0.346 ms | 0.00038 ms | 0.346 ms |
| S6 | 0.346 ms | 0.00038 ms | 0.346 ms |
| S14 | 0.346 ms | 0.00038 ms | 0.346 ms |
| P50 | 0.346 ms | 0.00044 ms | 0.346 ms |
| Full-field local GLS | 0 ms | 0.0120 ms | 0.0120 ms |

The shared compact extraction implementation computed the complete feature hierarchy together, so its timing is conservative and does not separate individual feature costs. The result demonstrates no computational advantage. It must not be generalized to optimized or nonlinear production estimators.

## 19. Negative Controls

Control A passed: full-field derivatives for `alpha` and `beta` were nonzero and the full Fisher matrix had rank four, while S2 was effectively blind to both zero-preserving modes. Control B passed at the claimed level: non-unit complex gain did not change the noiseless normalized compact states. Additive offsets and spatial calibration errors were not tested.

## 20. Failure Modes

- Local affine position extraction discarded global translation information relative to the efficient full-field estimate.
- The Jacobian at the zero contains essentially no first-order evidence for radial phase curvature and very weak evidence for envelope anisotropy after gain normalization.
- The selected polynomial descriptor and 5x5 patch were too local for modes whose evidence accumulates across the envelope.
- Local covariance pseudoinverses and finite differences require tolerance choices; rank-deficient estimates are therefore interpreted qualitatively and by multiple metrics.
- The local-linear estimator does not test global recovery, model mismatch, additive offsets, calibration slopes, or physical direct acquisition.

## 21. Interpretation

Zero-preserving modes can be represented in a compact parameter vector, but the tested singularity-centered measurements did not retain their information compactly. The strongest positive result is that a deterministic 14-value, gain-invariant descriptor remained measurable with zero extraction failures. The strongest negative result is that it retained only 8.84% joint information and only about 0.01% for the weakest required deformation mode.

## 22. Simulation Gate 2 Verdict

**FAIL**

No tested compact state retained enough multi-mode information. The result selects project outcome D for this exact broader task: abandon the tested compact singularity-centered states rather than claim a general compact sensing architecture.

## 23. Required Next Work

Do not proceed to 3D, experiment, paper drafting, or hardware. If Carson authorizes further work, the scientifically useful next step is a bounded reformulation gate asking whether deliberately nonlocal radial summaries or multiple spatially separated singularities can capture zero-preserving modes. That would be a new architecture, not a rescue of the failed local-state claim.

No 3D simulation, experiment, or paper was performed. No physical acquisition compression was demonstrated.
