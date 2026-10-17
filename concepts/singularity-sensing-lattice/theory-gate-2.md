# Theory Gate 2: Singularity-Anchored Multiscale Sampling

## 1. Objective

Determine whether the field singularity can serve as a spatial reference origin for a compact set of nonlocal radial and angular summaries that locally identifies translation, anisotropy, and radial phase curvature. This is a theory gate. It introduces no Monte Carlo campaign, simulation architecture, 3D model, hardware design, experiment, or paper draft.

## 2. Prior Evidence

- Gate 1B showed that, for the matched bounded translation model, the exact zero coordinate can encode translation essentially losslessly.
- Gate 2 showed that local compact states failed on the four-parameter family. S14 retained 8.84% joint information, its weakest required mode retained about 0.01%, and the normalized 5x5 patch retained 7.70%. Evidence for the zero-preserving modes accumulated outside the local neighborhood.
- Gate 3 showed that distributed product-field zero coordinates did not recover the missing information. The best practical joint retention was 15.98%, the ideal coordinate ceiling was 17.43%, count did not help, and large networks became unstable.

The new hypothesis therefore changes the retained statistic. The zero supplies an origin; nonlocal modal summaries carry deformation information.

## 3. Field Model

The primary testbed is the Gate 2 field

`Psi(u,v)=g (u+i v) exp(-[(1+alpha)u^2+(1-alpha)v^2]/(2 sigma^2)) exp(i beta (u^2+v^2)/sigma^2)`,

where `u=x-dx`, `v=y-dy`, `g=A exp(i phi)` is an unknown nonzero global complex gain, and the target is

`theta=[dx,dy,alpha,beta]`.

The analysis assumes `sigma>0`, bounded real `alpha` and `beta`, an isolated simple zero, complete calibrated circular summaries, and radii strictly greater than zero.

## 4. Singularity-Anchored Coordinates

The field has its unique admitted zero at

`(x_s,y_s)=(dx,dy)`.

Set `u=r cos(vartheta)`, `v=r sin(vartheta)`, and `rho=r^2/sigma^2`. Centering the polar coordinates on `(x_s,y_s)` removes `dx` and `dy` from the deformation field exactly under the analytical model. Translation remains available through the two zero coordinates.

## 5. Translation / Deformation Factorization

The ideal state factors as

`S(theta)=[x_s,y_s,D_alpha(alpha),D_beta(beta)]`.

The first block is `[dx,dy]`. The second block is computed in singularity-centered coordinates and is therefore translation invariant under exact centering. This is a clean factorization for the admitted field family, not a general claim for arbitrary fields or imperfect localization.

## 6. Polar Decomposition

The quadratic envelope term satisfies

`(1+alpha)u^2+(1-alpha)v^2`

`=r^2[(1+alpha)cos^2(vartheta)+(1-alpha)sin^2(vartheta)]`

`=r^2[1+alpha cos(2 vartheta)]`.

Therefore

`Psi(r,vartheta)=g r exp(-rho/2) exp(i vartheta) exp[-alpha rho cos(2 vartheta)/2] exp(i beta rho)`.

This identity is the central separation: `alpha` changes angular structure through `cos(2 vartheta)`, while `beta` changes radial phase through `rho`.

## 7. Angular Harmonic Structure

Define

`A_m(r)=(1/(2 pi)) integral_0^(2 pi) Psi(r,vartheta) exp(-i m vartheta) d vartheta`.

Let `z=alpha rho/2` and `B(r)=g r exp(-rho/2) exp(i beta rho)`. The standard expansion

`exp[-z cos(2 vartheta)]=sum_k (-1)^k I_k(z) exp(i 2 k vartheta)`

gives the exact coefficients

`A_(1+2k)(r)=B(r)(-1)^k I_k(z)`.

All even harmonics vanish in the exactly centered analytical model. In particular,

- `A_1=B I_0(z)` carries the base vortex and radial phase;
- `A_3=A_(-1)=-B I_1(z)` carries the leading anisotropy response;
- higher odd harmonics contain nonlinear anisotropy terms.

Near `alpha=0`, `I_0(z)=1+O(z^2)` and `I_1(z)=z/2+O(z^3)`, so

`A_3/A_1=-alpha rho/4+O(alpha^3 rho^3)`.

Thus `alpha` is naturally a quadrupolar modulation of the base `m=1` vortex, observed in the sidebands `m=-1` and `m=3`. The harmonic index is not `m=2` because the vortex factor shifts the second-angular-order envelope modulation by the base charge `+1`.

## 8. Radial Phase Structure

For real `alpha`, `I_0(alpha rho/2)` is positive. Consequently the phase of `A_1(r)` is

`arg A_1(r)=arg g+beta rho` modulo `2 pi`.

For distinct radii `r_i` and `r_j`,

`C_beta(i,j)=A_1(r_i) A_1(r_j)^*/(|A_1(r_i)||A_1(r_j)|)=exp[i beta(rho_i-rho_j)]`.

On an admitted local phase branch,

`D_beta=arg C_beta(i,j)/(rho_i-rho_j)=beta`.

Beta is therefore identifiable from a phase difference between two radial shells. The construction requires nonzero `A_1`, distinct radii, calibrated relative shell phase, and `|beta(rho_i-rho_j)|<pi` or an independently justified phase-unwrapping rule.

## 9. Candidate Summary Operators

The minimal operators are:

1. singularity localization for `x_s,y_s`;
2. one circular `m=1` projection and one `m=3` projection at radius `r_a`;
3. `m=1` projections at two distinct radii `r_i,r_j`.

The radius `r_a` may equal one of the beta radii, so only two distinct shells are required. A redundant practical candidate can add `A_(-1)`, a second alpha-sensitive radius, and a third beta radius for consistency checks.

## 10. Gain-Invariant Construction

Define the real anisotropy feature

`D_alpha(r_a)=Re[A_3(r_a)/A_1(r_a)]=-I_1(alpha rho_a/2)/I_0(alpha rho_a/2)`

and the phase-difference feature `D_beta` from Section 8. Both cancel the amplitude and phase of nonzero `g`. `D_alpha` also cancels the common radial phase. `D_beta` cancels real positive envelope and Bessel factors.

Admissibility requires `g!=0`, `r_a,r_i,r_j>0`, `A_1` above the measurement noise floor, `r_i!=r_j`, a locally unambiguous phase branch, and no detector saturation. Ratios must be rejected rather than evaluated when their denominator fails a predefined magnitude floor.

## 11. Minimal Candidate State

The smallest locally identifiable candidate is the four-real-value state

`S4=[x_s,y_s,D_alpha(r_a),D_beta(r_i,r_j)]`.

This is the mathematical minimum for four real target parameters. A six- to ten-value state would add shell and harmonic redundancy for noise, phase-unwrapping, and centering diagnostics, but redundancy is not required for nominal local rank.

## 12. Identifiability Matrix

At `alpha=0`, with `D_beta` divided by `rho_i-rho_j` as defined above,

`J_S=partial S4/partial[dx,dy,alpha,beta]`

`=diag(1,1,-rho_a/4,1)`.

Its determinant is `-rho_a/4`, which is nonzero for every admitted `r_a>0`. The state is full column rank four. Translation, anisotropy, and radial phase curvature occupy separate rows, so no nominal structural blind mode remains.

This result follows directly from the displayed field and Bessel identities. No computer algebra or numerical rank tolerance is needed. Reproducibility consists of substituting `u=r cos(vartheta)`, `v=r sin(vartheta)`, applying `cos^2-sin^2=cos(2 vartheta)`, expanding the exponential in modified Bessel harmonics, and using `I_1(z)/I_0(z)=z/2+O(z^3)`.

A deterministic quadrature sanity check used 32,768 uniform angles, `sigma=1`, `alpha=0.12`, `beta=0.17`, `g=1.7 exp(0.83 i)`, and radii 1.1 and 1.8. It recovered `D_beta=0.170000000000`, bounded the nominal even-harmonic magnitude by `6.94e-17`, and produced the finite-difference Jacobian `diag(1,1,-0.3025,1)` with rank four and condition number 3.3058. The check was executed in memory, used no random sampling, and created no result artifact.

## 13. Conditioning

Raw conditioning depends on parameter units and summary noise. If translation is nondimensionalized by `sigma`, the nominal unweighted Jacobian has diagonal magnitudes `1,1,rho_a/4,1`. Choosing `rho_a` near 4 balances those derivatives algebraically. That does not prove optimal statistical conditioning because the field magnitude decays as `r exp(-rho/2)` and shell noise depends on acquisition and integration.

The correct design objective is a noise-weighted criterion such as the minimum singular value or determinant of `J_S^T Sigma_S^-1 J_S`. The analytical rank is robust, but useful conditioning across the bounded operating region remains unverified.

## 14. Centering Error

Let the adopted origin differ from the true zero by a small complex displacement `epsilon`. Translating an odd-harmonic centered field by `epsilon` changes angular order by `+1` or `-1` at first order. The resulting leakage is therefore into even harmonics such as `m=0,2,4`, not into the odd `m=1,3,-1` channels used by `S4`.

With complete circular integration and the admitted smooth field, the chosen odd-harmonic deformation summaries are first-order insensitive to a small origin error at the nominal point. Their leading self-channel bias is second order in `|epsilon|/r`, while the reported translation coordinates themselves retain first-order localization error. Cross-terms with nonzero deformation, incomplete angular sampling, clipping, and calibration asymmetry can break this parity protection. Centering robustness is therefore promising but not established under realistic extraction noise.

## 15. Local vs Nonlocal Sensitivity

At the nominal point,

`partial Psi/partial alpha=-(rho/2) cos(2 vartheta) Psi`,

`partial Psi/partial beta=i rho Psi`.

Both deformation derivatives vanish relative to `Psi` as `r^2` near the zero. Since `|Psi|^2` is proportional to `r^2 exp(-rho)`, pointwise squared deformation sensitivity scales as `r^6 exp(-rho)`, and an annular integral adds another factor of `r`, giving `r^7 exp(-rho)`. The pointwise factor peaks at `rho=3`; the annular factor peaks at `rho=7/2` under uniform detector-noise weighting.

This explains why a tiny local patch can discard most alpha and beta evidence while nonlocal shells can target radii where their derivatives are large. It does not establish retained Fisher percentages, because shell covariance and nuisance projection have not been evaluated.

## 16. Radial Spacing Families

- **Uniform:** Simple and effective over a narrow known radial interval. It can allocate too many shells where the response is redundant.
- **Logarithmic or geometric:** Covers a broad multiplicative range efficiently, but may cluster shells near the origin where alpha and beta sensitivity is weak.
- **Golden-ratio:** A geometric grid with the fixed ratio `(1+sqrt(5))/2`. It supplies broad scale separation but no field-specific optimality.
- **Optimized:** Selects radii using a declared noise-weighted objective and admissible interval. For this low-order model, endpoint separation for beta and the signal-versus-`rho` tradeoff for alpha provide direct model-based criteria.

No spacing family dominates without a radius interval, shell covariance, sample budget, and objective. Uniform and ordinary geometric grids are legitimate baselines; optimized spacing is the principled candidate once a noise model is fixed.

## 17. Golden-Ratio Analysis

The field contains smooth low-order dependence on `rho=r^2/sigma^2`. Beta phase increments depend only on differences in `rho`; alpha sensitivity is monotone at small `alpha` before signal decay is considered. Neither expression singles out the golden ratio.

Irrationality alone does not improve local rank. Avoiding repeated phase increments can be useful in a broad phase-unwrapping problem, but any suitably noncommensurate or optimized set can do so. A fixed ratio of `phi` may also place shells outside the high-signal region or cluster an insufficient number within it. The actual measurement model therefore provides no special analytical advantage for golden-ratio spacing.

## 18. Analytical Noise Model

For a local theory model, let the real representation of the admitted modal summaries have covariance `Sigma_S`, positive definite after removal of deterministic redundancies. Then

`I_S=J_S^T Sigma_S^-1 J_S`.

Under independent equal-variance angular samples, circular projection variance falls approximately with the number of samples contributing to a shell. Real devices can introduce correlated shell noise, interpolation error, phase-reference drift, and radius-dependent signal-to-noise ratio. Those effects can change optimal radii and conditioning, so no numerical information-retention percentage is claimed here.

## 19. Fisher-Information Implications

Because `J_S` is full rank and gain invariant on the admitted branch, `I_S` is positive definite whenever `Sigma_S` is positive definite. This establishes local identifiability in the summary space. Data processing still requires `I_S` not to exceed the efficient full-field information when summaries are extracted from the same field. Whether the four-value state retains a useful fraction of that information is the decisive simulation question left open.

## 20. Candidate Dimensionality

- `S4`: two zero coordinates, one alpha ratio, one beta phase-slope feature. Dimension 4 and nominally full rank.
- `S6`: add one redundant alpha shell and one redundant beta phase difference. Dimension 6.
- `S8` to `S10`: add `m=-1` symmetry checks, a third radius, or denominator-quality observables.

All are far below 1,922 real full-field values as candidate post-extraction states. This is not detector or acquisition compression because dense field data may still be required to compute them.

## 21. Direct-Acquisition Implication

Classification: **A, direct modal acquisition is plausible in principle**. Annular coherent integration, phase-sensitive ring measurements, or modal projection channels could in principle produce `A_1` and `A_3` without reconstructing every field sample. No hardware feasibility, calibration budget, or performance advantage is established. If dense reconstruction is required in practice, the realized classification becomes B.

## 22. Failure Modes

- Ratio denominators can approach the noise floor at poorly chosen radii.
- Beta is locally identifiable but globally phase wrapped without an admitted bound or unwrapping channel.
- Noise-weighted conditioning may be poor even when analytical rank is full.
- Origin error is only parity-protected to first order for complete calibrated circular summaries.
- Finite angular sampling can alias harmonics and destroy the exact selection rules.
- Model mismatch can mix alpha and beta into additional channels.
- A compact post-extraction state does not establish acquisition or computational advantage.
- Optimized radii can overfit an assumed covariance or operating point.

## 23. Theory Gate 2 Verdict

**CONDITIONAL PASS**

The theory explicitly supplies a four-real-value, gain-invariant, full-rank local state for `[dx,dy,alpha,beta]`. Alpha and beta occupy distinct nonlocal channels, and no nominal structural blind mode remains. A bounded simulation is scientifically justified. The verdict is conditional because noise-weighted conditioning, phase wrapping, finite sampling, centering error outside the ideal parity argument, and retained information relative to the full field remain unresolved.

## 24. Golden-Ratio Sub-Verdict

**NO SPECIAL ADVANTAGE FOUND**

Golden-ratio radii are one fixed geometric choice. The analytical field model does not privilege `phi`, and model-based optimized or ordinary uniform/geometric spacing can be equally good or better depending on the admitted interval and noise covariance.

## 25. Required Next Work

If separately authorized, define a bounded 2D simulation gate that compares `S4`, `S6`, and a small redundant state against the efficient full-field benchmark. It should predefine radius bounds, angular sampling, denominator floors, beta phase range, centering perturbations, correlated summary covariance, and uniform, geometric, golden-ratio, and optimized radius sets under one common information criterion.

No new simulation was run. No 3D work, experiment, hardware design, paper drafting, commit, or push occurred.
