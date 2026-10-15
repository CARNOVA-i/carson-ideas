# Simulation Gate 1B: Singularity-State Information Ceiling

## 1. Objective

Determine whether Simulation Gate 1's approximately 14% translation-information retention was primarily an inefficient zero extractor or an inherent limit of the two-coordinate zero-position state. This gate remains confined to the published bounded 2D translation model.

## 2. Decision Thresholds

The following engineering bands were fixed before the final comparison:

- \(R_{ideal}\geq0.70\): strong support for the coordinate representation;
- \(0.40\leq R_{ideal}<0.70\): potentially useful but task-dependent;
- \(0.20\leq R_{ideal}<0.40\): weak or niche support only; and
- \(R_{ideal}<0.20\): strong evidence that the coordinate-only state is too lossy for this task.

These are decision thresholds, not universal scientific laws.

## 3. Baseline from Simulation Gate 1

The published Gate 1 verdict remains **HOLD**. Its 5x5 local affine extractor retained 14.03% of matched full-field efficient Fisher information on average, reduced the post-extraction representation from 1,922 real values to 2 coordinates, and produced 2.7 to 3.6 times higher combined translation RMSE than profile full-field estimation.

## 4. Field and Detector Model

Gate 1B reuses the translated 2D Gaussian-envelope vortex, 31x31 detector, 961 complex samples, circular complex Gaussian noise, translation \((0.17,-0.13)\), four SNR values (40, 30, 20, and 10 dB), three gain amplitudes, three gain phases, and fixed seed `20261015`. No physical or statistical model was changed.

The main comparison uses 160 paired trials in each of 36 conditions, for 5,760 trials. A bounded sensitivity study uses 300 trials at 30 dB for 21x21, 31x31, and 41x41 grids and affine windows of 3x3, 5x5, and 7x7.

## 5. Full-Field Information Ceiling

The benchmark is the same efficient Fisher matrix for translation after Schur-complement elimination of unknown complex gain. The competitive estimator is the same profile maximum-likelihood fit used in Gate 1. It uses all complex samples and analytically eliminates gain at every candidate translation.

## 6. Ideal Zero-State Model

For this restricted family, the field zero is exactly

\[
\mathbf z=(x_s,y_s)^T=(\Delta x,\Delta y)^T=\boldsymbol\theta.
\]

The coordinate map is one-to-one and has identity Jacobian. A two-coordinate output is therefore not inherently lossy for the translation-only target. An efficient coordinate estimator derived from the sampled likelihood can asymptotically attain the full-field efficient Cramer-Rao bound.

This does not mean a magical noiseless zero is observed. It means the finite sampled data can be processed into an efficient two-coordinate estimate for this specified model. It also does not make the coordinate sufficient for other perturbations.

## 7. Zero-State Fisher Information / CRB

The defensible sampled-grid ceiling is

\[
\mathbf I_{zero,ideal}=\mathbf I_{full,eff},
\qquad R_{ideal}=1.
\]

The improved practical extractor is a global profile-likelihood zero localizer. It starts from the measured-field minimum within the admitted search region, uses no true-parameter initialization, eliminates complex gain analytically, and emits only the fitted zero coordinate.

Its raw empirical trace retention averaged 1.010. Values slightly above one at finite trial count are Monte Carlo covariance error, not information creation. The physical result is capped by data processing at 1.0. Eigenvalue-wise raw retention across SNRs remained close to unity, spanning approximately 0.930 to 1.057.

## 8. Finite-Sampling Effects

A separate continuous-field ceiling cannot be assigned without a direct continuous-zero measurement noise model. Under the actual finite sampled-grid model, profile coordinate localization retained 98.1%, 99.9%, and 94.9% raw empirical trace information for 21x21, 31x31, and 41x41 grids at 30 dB. These deviations are consistent with finite Monte Carlo estimation around the analytical 100% ceiling.

The coordinate representation itself is therefore not limited to approximately 14% by detector sampling. Local estimator design and the physical size of its selected window matter far more.

## 9. Improved Zero Extractor

The improved extractor is the profile-likelihood coordinate fit described above. It is transparent and statistically matched to the known vortex family. It is also computationally equivalent to the full-field estimator, although its retained state is only two numbers.

Mean runtime was approximately 2.70 ms per estimate on this machine. It had zero failures in all 5,760 main trials.

## 10. Existing Gate 1 Extractor

The Gate 1 method remains the measured-minimum initialization followed by independent local affine fits to real and imaginary field components over a 5x5 window. The implementation compatibility check passed exactly.

In the larger Gate 1B paired run it retained 12.47% on average, close to the published 14.03% estimate. The difference is attributable to Monte Carlo sample size and does not reinterpret the published result.

## 11. Monte Carlo Protocol

- Fixed seed: `20261015`
- Identical noisy samples for all extractors in each trial
- 5,760 main trials across the original 36 conditions
- Second-moment information approximation includes estimator bias
- 900 additional grid-sensitivity trials
- All decision bands fixed before results were evaluated

## 12. Information-Ceiling Results

| Level | Trace retention | Interpretation |
|---|---:|---|
| Full-field efficient benchmark | 100% | Reference |
| Ideal two-coordinate zero state | 100% | Analytical ceiling for translation-only family |
| Profile-likelihood zero extractor | 100% physical ceiling; 101.0% raw empirical mean | Reaches ceiling within Monte Carlo error |
| Gate 1 affine 5x5 extractor | 14.03% published; 12.47% Gate 1B paired run | Strong extraction loss |

Raw profile retention by SNR was 103.1%, 98.5%, 104.1%, and 98.4% at 40, 30, 20, and 10 dB. Values above 100% are explicitly treated as finite-sample covariance error and not as physical information gain.

## 13. Representation Loss

For the specified two-parameter translation family, ideal representation loss is 0% because the zero coordinate is the target parameter itself. This conclusion is narrow. The negative control proves that representation loss becomes 100% for at least one zero-preserving deformation.

## 14. Extraction Loss

Relative to the 100% coordinate ceiling, the published Gate 1 extractor loses approximately 86% of task information. The larger Gate 1B paired estimate gives 87.5% loss. The profile estimator's apparent mean loss is 0% after enforcing the physical information ceiling; its 1.0% raw excess is Monte Carlo error.

Thus the approximately 14% Gate 1 result is primarily an extractor limitation for 2D translation under this model.

## 15. Grid / Window Sensitivity

At 30 dB, trace retention was:

| Grid | Profile | Affine 3x3 | Affine 5x5 | Affine 7x7 |
|---:|---:|---:|---:|---:|
| 21x21 | 98.1% | 8.3% | 5.9% | 1.8% |
| 31x31 | 99.9% | 5.4% | 13.7% | 20.6% |
| 41x41 | 94.9% | 3.0% | 8.0% | 12.9% |

The local affine result is not monotonic with grid density because a fixed pixel window changes physical width and trades noise averaging against curvature bias. At the principal 31x31 grid, expanding from 5x5 to 7x7 improved mean retention from 12.47% to 20.01%, but remained far below the profile ceiling. No best window was selected after the fact; all tested values are reported.

## 16. Estimator Performance

| SNR | Profile RMSE | Affine 5x5 RMSE | Profile failures | Affine 5x5 failures |
|---:|---:|---:|---:|---:|
| 40 dB | 0.000371 | 0.001373 | 0% | 0% |
| 30 dB | 0.001201 | 0.003230 | 0% | 0% |
| 20 dB | 0.003693 | 0.009526 | 0% | 0% |
| 10 dB | 0.012027 | 0.037373 | 0% | 0.139% |

Across the recorded runs, mean profile-localization time ranged from approximately 2.70 to 3.07 ms; affine ranges were 0.214 to 0.252 ms for 3x3, 0.179 to 0.197 ms for 5x5, and 0.173 to 0.187 ms for 7x7. These are implementation-specific wall-clock measurements and do not affect the deterministic numerical results.

Bias, axis-specific RMSE, condition numbers, eigenvalue ratios, and condition-level failures are recorded in the CSV.

## 17. Negative Control

The Gate 1 zero-preserving radial deformation remains observable in the full field and invisible to the exact zero coordinate. Even ideal extraction yields zero coordinate information for that mode. This is a representation limit, not an extractor defect.

## 18. Direct Feature Acquisition Implication

Dedicated hardware that directly measured the zero coordinate would change acquisition and detector-burden accounting only after its own noise likelihood was specified. It would not change the coordinate state's task mapping: 100% for this ideal translation-only family and 0% for the zero-preserving negative-control mode. No direct-feature hardware feasibility is established here.

## 19. Failure Modes

- The 100% ceiling depends on the exact translation-only model and matched likelihood.
- The profile extractor obtains efficiency by using the complete sampled field and has no demonstrated acquisition or compute advantage.
- Empirical inverse second moments fluctuate around the Fisher bound at finite trial count.
- Fixed pixel windows change physical size across grids.
- Model mismatch, additive backgrounds, spatial gain, calibration error, and relative phase remain untested.
- A two-coordinate state cannot represent perturbations that leave the zero fixed.

## 20. Interpretation

Gate 1's approximately 14% result was primarily caused by the local affine extractor, not an inherent translation-information ceiling of the two-coordinate state. The improved profile coordinate estimate preserves essentially all matched task information, but does so by processing all 961 complex samples with the same likelihood as the full-field estimator.

The result supports state compression and ideal common-gain invariance. It does not support measurement compression, detector reduction, bandwidth reduction before extraction, or lower computation for the efficient method. For broader inverse reconstruction, the negative control prevents generalization from this translation-only result.

## 21. Simulation Gate 1B Verdict

**PASS**

The ideal zero-coordinate state exceeds the predefined 70% threshold and the improved transparent extractor reaches the full-field ceiling within Monte Carlo error. The representation provides defensible post-extraction dimensional reduction and common-gain invariance for this bounded translation task. The pass applies only to the information-ceiling question, not to the overall 3D concept or practical acquisition architecture.

## 22. Required Next Work

1. Do not enrich the state merely to improve translation estimation; the two coordinates are already adequate under the matched model.
2. Before broader claims, specify a multi-parameter target family containing realistic zero-moving and zero-preserving modes.
3. Test whether a cheaper local likelihood or dedicated acquisition model can approach the ceiling without full-field computation.
4. Add additive background, spatial-gain, calibration, and relative-phase mismatch.
5. Keep 3D work and paper drafting on hold pending separate authorization and a defensible broader-task result.

No 3D simulation was performed, no experiment was performed, and no paper was written.
