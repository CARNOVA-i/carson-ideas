# Simulation Gate 1: 2D Information Retention

## 1. Objective

Test whether a two-coordinate singularity state, extracted from the same noisy complex-field samples used by a competitive full-field estimator, retains enough information about two-dimensional translation to justify further work. This is a bounded numerical test, not evidence for a 3D lattice, an experiment, or a general sensing advantage.

## 2. Hypothesis

For a translated isolated zero, its coordinate should encode translation and be invariant to a nonzero global complex gain. The extracted coordinate may therefore provide extreme dimensional reduction and nuisance invariance, but data processing requires it to contain no more translation information than the complete sampled field.

## 3. Field Model

The simulated complex scalar field is

\[
\Psi(x,y;\boldsymbol\theta,g)=g[(x-\Delta x)+i(y-\Delta y)]
\exp\left[-\frac{(x-\Delta x)^2+(y-\Delta y)^2}{2\sigma^2}\right],
\]

with \(\boldsymbol\theta=(\Delta x,\Delta y)=(0.17,-0.13)\), \(\sigma=1.15\), and nonzero complex gain \(g=Ae^{i\phi}\). The model has one stable isolated zero at \(\boldsymbol\theta\), is analytically transparent, and avoids an unnecessary propagation model.

## 4. Detector Model

A uniform \(31\times31\) grid covers \([-2.5,2.5]^2\), giving 961 complex samples or 1,922 real values. Both estimators receive exactly the same noisy grid. The admitted translation search region is \([-0.6,0.6]^2\), which prevents the Gaussian envelope's low-amplitude detector edges from being mistaken for the field zero.

## 5. Noise Model

Each sample is

\[
y_k=\Psi(x_k,y_k;\boldsymbol\theta,g)+n_k,
\]

where \(n_k\) is independent circular complex Gaussian noise. The reported variance is \(\sigma_n^2=\mathbb E|n_k|^2\); real and imaginary components each have variance \(\sigma_n^2/2\). SNR is

\[
10\log_{10}\frac{\operatorname{mean}|g\Psi_0|^2}{\sigma_n^2}.
\]

The sweep uses 40, 30, 20, and 10 dB.

## 6. Nuisance Parameters

The gain amplitudes are 0.7, 1.0, and 1.4; phases are 0, 0.9, and 2.1 radians. Noise is scaled to preserve the specified SNR for each amplitude. Multiplication by any nonzero \(g\) leaves the analytical zero unchanged. The full-field estimator treats both real components of \(g\) as unknown nuisance parameters.

## 7. Full-Field Estimator

For each trial, nonlinear least squares searches over \((\Delta x,\Delta y)\). At every candidate translation, the complex gain is eliminated analytically:

\[
\widehat g=\frac{\mathbf f(\boldsymbol\theta)^H\mathbf y}{\mathbf f(\boldsymbol\theta)^H\mathbf f(\boldsymbol\theta)}.
\]

This is the profile maximum-likelihood estimator under the stated Gaussian noise. It uses every detector sample and does not assume the nuisance gain is known. Convergence requires a finite solution inside the admitted translation region.

## 8. Singularity-State Estimator

The minimum-magnitude sample is selected within the admitted translation region. A \(5\times5\) neighborhood is fitted with independent affine planes for the real and imaginary field components. Their fitted zero-contour intersection is the singularity estimate. A trial is rejected if the local Jacobian condition number exceeds \(10^5\), the intersection is nonfinite, falls outside the local window, or leaves the detector.

The baseline zero is \((0,0)\), so the estimated zero coordinate directly estimates translation. Ideal global gain rotates and scales both fitted field components without moving their common analytical zero. Noise, curvature, grid selection, and affine-model mismatch still affect the extracted coordinate.

## 9. Fisher Information

For parameters \((\Delta x,\Delta y,g_R,g_I)\), the full Gaussian Fisher matrix is computed from numerical field derivatives:

\[
\mathbf I=\frac{2}{\sigma_n^2}\operatorname{Re}(\mathbf J^H\mathbf J).
\]

Efficient translation information is the Schur complement of the two-dimensional gain block. Symmetry and positive semidefiniteness are checked numerically.

For the singularity state, information is approximated as the inverse empirical covariance of successful coordinate errors within each 80-trial condition. This Gaussian local approximation does not model selection failures and has Monte Carlo uncertainty. It is therefore an estimator-specific approximation, not a proof of the maximum information available in every possible zero-extraction algorithm.

## 10. Monte Carlo Protocol

- Fixed seed: `20261015`
- 4 SNR values
- 3 gain amplitudes
- 3 gain phases
- 80 paired trials per condition
- 36 conditions and 2,880 total trials
- Identical noisy samples supplied to both estimators in each trial

The script is command-line runnable and writes the CSV, JSON summary, and all figures without manual editing.

## 11. Results

Values below average the nine gain conditions at each SNR. Coordinates are in detector-axis units.

| SNR (dB) | Full RMSE x | Full RMSE y | Full combined RMSE | Singularity RMSE x | Singularity RMSE y | Singularity combined RMSE | Information ratio |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 40 | 0.000256 | 0.000277 | 0.000377 | 0.000687 | 0.001155 | 0.001345 | 0.157 |
| 30 | 0.000822 | 0.000844 | 0.001179 | 0.002209 | 0.002309 | 0.003198 | 0.155 |
| 20 | 0.002575 | 0.002560 | 0.003641 | 0.006930 | 0.007088 | 0.009924 | 0.150 |
| 10 | 0.008607 | 0.008589 | 0.012193 | 0.027231 | 0.027174 | 0.038553 | 0.099 |

Full-field mean biases in either axis remain below 0.00040. Singularity mean biases remain below 0.00094 in magnitude. Full-field failure rate is 0. Singularity localization has one failure in 2,880 trials, a total rate of 0.000347 and a 10 dB mean rate of 0.001389.

The full-field RMSE closely follows its calculated Cramér-Rao standard deviations. For example, at 10 dB the averaged axis bounds are 0.008427 and 0.008422, compared with RMSE values 0.008607 and 0.008589.

## 12. Information Retention

The trace ratio \(\operatorname{tr}(\mathbf I_S)/\operatorname{tr}(\mathbf I_{\mathrm{eff,full}})\) averages 0.140 across all conditions, ranges from 0.081 to 0.189 condition by condition, and declines from about 0.156 at 40 dB to 0.099 at 10 dB. The tested local affine singularity estimator therefore discards most available translation information.

The state itself is extremely compact: 2 real coordinates replace 1,922 real detector values, a 961:1 dimensional reduction after extraction. This does not reduce the simulated measurement burden because the zero was derived from the full grid.

## 13. Nuisance Invariance

The analytical zero is exactly invariant to every tested nonzero common amplitude and phase. The noiseless implementation check confirms that multiplying the sampled field by \(1.7e^{1.3i}\) does not change the estimated zero to numerical tolerance. Under fixed relative SNR, all nine gain settings produce the same qualitative RMSE and information ordering. The full-field estimator also handles the gain correctly through analytical nuisance elimination.

This establishes ideal common-gain invariance within the model. It does not cover additive offsets, saturation, spatially varying gain, relative source-phase drift, calibration errors, or reconstruction errors.

## 14. Negative Control

The negative control multiplies the field by

\[
1+q\frac{r^2}{\sigma^2},
\]

with \(q\) varied between -0.25 and 0.25. This changes nonzero field samples but leaves the analytical zero fixed. At 30 dB the full field has positive efficient information about \(q\) (approximately \(2.99\times10^6\) in the chosen parameterization), while the exact zero coordinate has zero information. The local affine extractor shifts by 0.000958 between the two noiseless cases because curvature changes its approximation bias, not because the physical zero moved. This is estimator mismatch, not reliable singularity information.

The control demonstrates the intended failure: one zero coordinate cannot identify a zero-preserving deformation that the complete field can measure.

## 15. Computational Cost

Across the authoritative recorded invocation, mean Python runtime per estimate was approximately 2.94 ms for profile nonlinear least squares and 0.220 ms for the local singularity fit, about a 13-fold difference on this machine and software stack. The pre-commit clean reproduction measured approximately 3.19 ms and 0.236 ms, respectively, preserving the same roughly 13-fold ordering. The full estimator repeatedly evaluates all \(M=961\) samples; the local fit solves two small least-squares systems after an \(O(M)\) search.

These timings are implementation-specific and exclude acquisition, complex-field reconstruction, data transfer, calibration, and feature association. Because both paths begin from the same full grid, they do not establish lower physical measurement cost.

## 16. Failure Modes

- The global magnitude minimum is invalid for an enveloped field because edges are dark; an admitted translation region is required.
- Local affine fitting loses information contained outside the neighborhood and incurs curvature bias.
- At low SNR, the minimum-sample selection becomes less stable and information retention declines.
- The empirical singularity Fisher estimate is limited by 80 samples per condition.
- Bounds and prior knowledge constrain both estimators and must be declared.
- Global-gain invariance does not imply invariance to realistic nonmultiplicative nuisances.
- State compression occurs after full-field acquisition in this experiment.
- A single zero is blind to zero-preserving deformation and cannot establish multimode rank.

## 17. Interpretation

Within the tested model, a singularity coordinate is a highly compact and exactly common-gain-invariant translation statistic. Its transparent local extraction is fast and remains usable over the tested SNR range. Those are real but narrow practical signals.

Under the same noisy detector samples, however, the tested singularity estimator is materially less efficient than the full-field profile likelihood. It retains only about 14% of efficient Fisher information on average and has roughly 2.7 to 3.6 times higher combined RMSE. The dimensional reduction is post-acquisition, so it does not yet lower detector burden. The negative control confirms a complete blind spot for zero-preserving deformation.

The results neither falsify the analytical claim that an ideal zero can encode translation nor demonstrate that an extracted zero is near-sufficient under sampled noise. A better extraction method could change the estimator-specific fraction, but data processing prevents it from exceeding the matched full-field information.

## 18. Simulation Gate Verdict

**HOLD**

The bounded simulation shows a plausible compression, nuisance-invariance, and computational benefit, but the tested extraction retains too little task-relevant information for `PASS` or `CONDITIONAL PASS`. The result is not an unqualified `FAIL` because the state is compact, gain-invariant, fast to estimate, and operational at all tested SNRs; estimator efficiency and direct-feature acquisition remain unresolved.

## 19. Required Next Work

1. Before any 3D work or paper drafting, test a statistically stronger zero-localization method derived from the same samples, with analytical or bootstrap covariance and a larger Monte Carlo budget.
2. Separate state-compression benefit from measurement burden by specifying whether hardware can estimate the zero without acquiring the complete complex field.
3. Add realistic additive background, spatial gain, calibration error, and relative-phase nuisance cases.
4. Test a minimal second feature only if it adds sensitivity rank rather than duplicated precision.
5. Predefine a quantitative retention threshold and practical cost target before rerunning the gate.

No 3D simulation was performed, no experiment was performed, and no theory paper was written.
