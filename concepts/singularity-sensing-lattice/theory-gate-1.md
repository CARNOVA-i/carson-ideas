# Theory Gate 1: Information and Identifiability

## 1. Objective

Determine whether a singularity-state representation can be a defensible sensing representation compared with direct complex-field measurement.

The gate is hostile by design. It tests whether singularity positions, trajectories, and topology retain enough task-relevant information to justify dimensional reduction, invariance, conditioning, classification, or practical measurement efficiency. Large singularity motion by itself is not a benefit.

This document contains analytical derivations and evaluation criteria. It is not a theory paper, numerical simulation, or experimental validation.

## 2. Field Model

Let

\[
\Psi(\mathbf r;\boldsymbol\theta,\boldsymbol\phi)\in\mathbb C
\]

be a differentiable complex scalar field. Here:

- \(\mathbf r\in\mathbb R^d\) is position;
- \(\boldsymbol\theta\in\mathbb R^p\) contains parameters of interest, such as displacement, target pose, refractive-index coefficients, or strain coefficients; and
- \(\boldsymbol\phi\in\mathbb R^q\) contains nuisance parameters, such as source gain, common phase, calibration drift, or environmental state not intended for estimation.

The field may be a physical field or a reconstruction produced by a specified measurement operator. Those cases are not interchangeable. If singularities are extracted from a filtered intensity image rather than from the physical complex field, the resulting state must be identified as a computed feature representation.

The field measurement is not assumed ideal. A generic model is

\[
\mathbf y_E=\mathcal M[\Psi(\cdot;\boldsymbol\theta,\boldsymbol\phi)]+\mathbf n_E,
\]

where \(\mathcal M\) includes aperture, sampling, projection, propagation, detector response, and any field-reconstruction algorithm.

## 3. Singularity Definition

Define the real map

\[
\mathbf F(\mathbf r,\boldsymbol\theta,\boldsymbol\phi)=
\begin{bmatrix}
\operatorname{Re}\Psi(\mathbf r;\boldsymbol\theta,\boldsymbol\phi)\\
\operatorname{Im}\Psi(\mathbf r;\boldsymbol\theta,\boldsymbol\phi)
\end{bmatrix}\in\mathbb R^2.
\]

A scalar phase singularity or field zero satisfies

\[
\mathbf F(\mathbf r_i,\boldsymbol\theta,\boldsymbol\phi)=\mathbf 0.
\]

The candidate discrete state is more accurately written as

\[
S=\{(\mathbf r_i,q_i,\mathbf J_i,\ell_i,\ldots)\}_{i=1}^{N},
\]

where \(q_i\) is topological charge, \(\mathbf J_i\) is the local spatial Jacobian, and \(\ell_i\) is an identity or association label. The position-only state loses information that may be necessary for conditioning, identity, and topology.

### Dimensional obstruction in three dimensions

For a generic complex scalar field in \(d=3\), \(\mathbf F:\mathbb R^3\rightarrow\mathbb R^2\). If the spatial Jacobian has rank two, the regular-value theorem implies that the zero set is locally a one-dimensional curve, not an isolated point. Therefore a “3D lattice of point singularities” is not generic.

A discrete 3D state requires at least one of:

- intersections with specified measurement planes or surfaces;
- identifiable landmarks along vortex or nodal lines;
- additional independent field constraints;
- engineered symmetry that creates isolated, generally fragile points; or
- a line/set representation rather than a point representation.

Tangential reparameterization along a regular zero line is a gauge freedom. Only normal displacement is fixed by the two zero constraints without an additional convention.

## 4. Local Perturbation Response

At a regular zero, perturb

\[
\boldsymbol\theta\mapsto\boldsymbol\theta+\delta\boldsymbol\theta,
\qquad
\mathbf r_i\mapsto\mathbf r_i+\delta\mathbf r_i.
\]

First-order expansion gives

\[
\mathbf J_i\delta\mathbf r_i+\mathbf K_i\delta\boldsymbol\theta=\mathbf 0,
\]

with

\[
\mathbf J_i=\left.\frac{\partial\mathbf F}{\partial\mathbf r}\right|_i
\in\mathbb R^{2\times d},
\qquad
\mathbf K_i=\left.\frac{\partial\mathbf F}{\partial\boldsymbol\theta}\right|_i
\in\mathbb R^{2\times p}.
\]

### Isolated regular zero in two dimensions

For \(d=2\), if \(\det\mathbf J_i\neq0\), the implicit-function theorem gives a locally unique zero and

\[
\delta\mathbf r_i=-\mathbf J_i^{-1}\mathbf K_i\delta\boldsymbol\theta.
\]

### Overdetermined or underdetermined coordinates

When \(\mathbf J_i\) is not square, a Moore–Penrose pseudoinverse gives the minimum-norm normal response

\[
\delta\mathbf r_i^{\perp}=-\mathbf J_i^+\mathbf K_i\delta\boldsymbol\theta.
\]

The general solution is

\[
\delta\mathbf r_i=-\mathbf J_i^+\mathbf K_i\delta\boldsymbol\theta
+(\mathbf I-\mathbf J_i^+\mathbf J_i)\mathbf w_i,
\]

where \(\mathbf w_i\) is arbitrary in the spatial null space. In 3D, this term is normally tangential motion along the zero line. It is not observable from the zero constraint alone.

### Rank and degeneracy

The local formula requires constant rank and a persistent feature identity. It fails or becomes unreliable when:

- \(\operatorname{rank}\mathbf J_i<2\);
- the smallest nonzero singular value of \(\mathbf J_i\) approaches zero;
- zeros merge, split, appear, disappear, or reconnect;
- a higher-order zero unfolds into several first-order zeros;
- the detector cannot localize the low-amplitude core; or
- the chosen line landmark changes discontinuously.

Creation and annihilation points are bifurcations, not large but ordinary linear responses. They require nonlinear local normal forms and event models.

## 5. Multi-Singularity Sensitivity Matrix

After defining observable coordinates for each feature, let

\[
\mathbf A_i=-\mathbf J_i^+\mathbf K_i.
\]

For isolated 2D zeros, \(\mathbf A_i\in\mathbb R^{2\times p}\). For 3D lines, \(\mathbf A_i\) must be restricted to defined normal coordinates or to explicit landmarks.

Stack the feature displacements:

\[
\Delta\mathbf S=
\begin{bmatrix}
\delta\mathbf r_1\\
\vdots\\
\delta\mathbf r_N
\end{bmatrix}
=
\underbrace{\begin{bmatrix}
\mathbf A_1\\
\vdots\\
\mathbf A_N
\end{bmatrix}}_{\mathbf H}
\delta\boldsymbol\theta+\boldsymbol\eta.
\]

The matrix \(\mathbf H\) is the linearized global sensitivity matrix.

Important diagnostics are:

- **Rank:** number of locally observable parameter combinations.
- **Null space:** perturbations that do not move the represented features to first order.
- **Singular values:** gain for orthogonal parameter modes.
- **Condition number:** worst relative amplification in inversion.
- **Row-space redundancy:** repeated singularities may add measurements without adding new modes.
- **Noise-weighted rank:** nominal rank is insufficient if informative modes lie below localization noise.

Adding a singularity cannot reduce the algebraic information in an ideal correctly modelled stack, but it may add no rank, worsen data association, introduce correlated noise, or increase calibration cost. Removing a singularity is harmless only if its noise-whitened sensitivity row lies in the span of the retained rows to the required accuracy.

With zero-mean localization noise covariance \(\boldsymbol\Sigma_S\), the generalized least-squares estimate is

\[
\widehat{\delta\boldsymbol\theta}
=(\mathbf H^T\boldsymbol\Sigma_S^{-1}\mathbf H)^{-1}
\mathbf H^T\boldsymbol\Sigma_S^{-1}\Delta\mathbf S,
\]

provided the inverse exists. Its linearized covariance is

\[
\operatorname{Cov}(\widehat{\delta\boldsymbol\theta})
=(\mathbf H^T\boldsymbol\Sigma_S^{-1}\mathbf H)^{-1}.
\]

## 6. Identifiability

### Local identifiability

Under fixed feature identities, differentiability, a regular zero set, and a correctly specified local model, \(\boldsymbol\theta\) is locally identifiable from the represented coordinates if the map \(\boldsymbol\theta\mapsto S\) is locally one-to-one.

For the linearized model, a necessary and locally sufficient first-order condition is

\[
\operatorname{rank}\mathbf H=p.
\]

This condition is not sufficient when:

- the derivative is full rank at an isolated point but the nonlinear map folds nearby;
- singularity labels can permute;
- symmetries produce equivalent unordered sets;
- nuisance parameters are omitted;
- features appear or disappear; or
- the observable coordinates include an arbitrary line gauge.

With nuisance sensitivities \(\mathbf B\delta\boldsymbol\phi\), the model becomes

\[
\Delta\mathbf S=\mathbf H\delta\boldsymbol\theta+\mathbf B\delta\boldsymbol\phi+\boldsymbol\eta.
\]

Parameters of interest are identifiable only if their noise-weighted sensitivity subspace is separable from the nuisance subspace. A useful test is the rank and smallest singular value of the projected matrix

\[
\mathbf P_{\mathbf B}^{\perp}\mathbf H,
\]

where the projection uses the appropriate noise metric.

### Global identifiability

Global identifiability requires

\[
S(\boldsymbol\theta_1)=S(\boldsymbol\theta_2)
\Longrightarrow
\boldsymbol\theta_1=\boldsymbol\theta_2
\]

over the admitted parameter domain, modulo explicitly accepted symmetries. Unordered sets create permutation symmetry. Mirror, rotation, common-phase, sign, and periodic ambiguities can produce identical states. Global injectivity must be proved or bounded; local rank cannot establish it.

## 7. Full-Field Comparison

Let

\[
\mathbf y_E=\boldsymbol\mu_E(\boldsymbol\theta,\boldsymbol\phi)+\mathbf n_E
\]

represent the actual full-field measurement channel. Let the singularity estimate be

\[
\mathbf y_S=G(\mathbf y_E,\boldsymbol\kappa)+\mathbf n_G,
\]

where \(G\) includes field reconstruction, zero localization, labelling, and topology extraction, and \(\boldsymbol\kappa\) contains calibration variables.

If \(\mathbf y_S\) is derived only from \(\mathbf y_E\), then

\[
\boldsymbol\theta\rightarrow\mathbf y_E\rightarrow\mathbf y_S
\]

forms a Markov chain. Under the same data and correctly specified likelihood, deterministic or stochastic post-processing cannot increase information about \(\boldsymbol\theta\). An optimal full-field estimator can always reproduce \(G\) internally and then use any remaining information.

Therefore the singularity representation cannot exceed the information content of the same complete field measurement. A valid advantage must instead be one of:

- near-sufficiency for a restricted parameter family with substantial data reduction;
- invariance to a nuisance that would otherwise require explicit modelling;
- better conditioning for a constrained non-optimal estimator;
- lower storage, transmission, or compute cost at an accepted accuracy loss;
- a different physical measurement channel that estimates zeros without first acquiring the same full field; or
- interpretable discrete events useful for classification or fault detection.

Comparisons against a poor full-field algorithm do not establish a representational advantage. The baseline must be an efficient estimator using the same raw measurements and nuisance model.

## 8. Fisher Information Framework

For observations \(\mathbf y\sim p(\mathbf y\mid\boldsymbol\theta)\), define

\[
\mathbf I(\boldsymbol\theta)=
\mathbb E\left[
\nabla_{\boldsymbol\theta}\log p(\mathbf y\mid\boldsymbol\theta)
\nabla_{\boldsymbol\theta}\log p(\mathbf y\mid\boldsymbol\theta)^T
\right].
\]

### Gaussian singularity-position model

If

\[
\mathbf y_S\sim\mathcal N(\mathbf s(\boldsymbol\theta),\boldsymbol\Sigma_S)
\]

and \(\boldsymbol\Sigma_S\) is locally parameter-independent, then

\[
\mathbf I_S=\mathbf H^T\boldsymbol\Sigma_S^{-1}\mathbf H.
\]

If covariance depends on the parameters, the standard Gaussian covariance-derivative term must also be included.

### Gaussian full-field model

For

\[
\mathbf y_E\sim\mathcal N(\boldsymbol\mu_E(\boldsymbol\theta),\boldsymbol\Sigma_E),
\]

with parameter-independent covariance and field sensitivity

\[
\mathbf D_E=\frac{\partial\boldsymbol\mu_E}{\partial\boldsymbol\theta},
\]

the Fisher information is

\[
\mathbf I_E=\mathbf D_E^T\boldsymbol\Sigma_E^{-1}\mathbf D_E.
\]

For a statistic derived from the same observations, the Fisher-information data-processing inequality gives

\[
\mathbf I_S\preceq\mathbf I_E
\]

under regularity conditions. Equality requires the singularity statistic to be sufficient for \(\boldsymbol\theta\) under the specified model, an exceptional claim that must be proved rather than presumed.

### Nuisance parameters

Partition the joint Fisher matrix for \((\boldsymbol\theta,\boldsymbol\phi)\). The efficient information for \(\boldsymbol\theta\) is the Schur complement

\[
\mathbf I_{\mathrm{eff}}
=\mathbf I_{\theta\theta}
-\mathbf I_{\theta\phi}
\mathbf I_{\phi\phi}^{-1}
\mathbf I_{\phi\theta},
\]

with generalized inverses when required. A singularity representation may suppress nuisance sensitivity, but an optimal full-field likelihood with the same nuisance model cannot be outperformed by discarding data. The practical question is whether the reduced statistic achieves nearly the same efficient information with materially lower cost or modelling burden.

### Required future comparison

For a selected physical architecture, calculate or estimate:

1. \(\mathbf I_E\) from the actual sampled measurement channel;
2. \(\mathbf I_S\) including localization and association uncertainty;
3. the generalized eigenvalues of \((\mathbf I_S,\mathbf I_E)\);
4. storage, bandwidth, and computation per estimate; and
5. robustness under matched and mismatched nuisance models.

## 9. Noise Propagation

Let an estimated zero experience a local residual perturbation \(\delta\mathbf F_i\). Linearization gives

\[
\mathbf J_i\delta\mathbf r_i+\delta\mathbf F_i=\mathbf 0.
\]

For a fixed gauge or minimum-norm normal displacement,

\[
\delta\mathbf r_i=-\mathbf J_i^+\delta\mathbf F_i.
\]

If

\[
\operatorname{Cov}(\delta\mathbf F_i)=\boldsymbol\Sigma_{F,i},
\]

then

\[
\boldsymbol\Sigma_{r,i}
\approx
\mathbf J_i^+\boldsymbol\Sigma_{F,i}(\mathbf J_i^+)^T.
\]

Cross-covariances between singularities must be retained because source phase noise, reconstruction error, and calibration drift are commonly correlated. Stacking independent per-feature covariances when the errors share a field source overstates information.

Noise mechanisms enter differently:

- **Additive complex-field noise:** perturbs both zero coordinates through \(\mathbf J_i^+\).
- **Phase noise:** common phase multiplication leaves exact zeros fixed, but spatially varying phase noise and reconstruction error move estimated zeros.
- **Amplitude drift:** a nonzero global complex scale leaves exact zeros invariant, which is a genuine invariance; additive offsets and saturation do not.
- **Source phase instability:** common phase is harmless to physical zero location, while relative source phase changes can move an interference-generated lattice strongly.
- **Detector noise:** localization is difficult near a dark core and depends on sampling, point-spread function, photon counts, and estimator bias.
- **Calibration error:** uncertainty in coordinates, propagation distance, optical transfer function, or antenna response creates structured, correlated feature motion.
- **Association error:** label swaps and missed births/deaths are non-Gaussian outliers, not small localization noise.

## 10. Sensitivity Versus Noise Amplification

Let \(\mathbf J_i=\mathbf U\boldsymbol\Sigma\mathbf V^T\). Then \(\mathbf J_i^+\) contains reciprocals of nonzero singular values. A small spatial singular value can produce a large apparent displacement for a fixed field perturbation:

\[
\|\delta\mathbf r_i\|\sim\frac{\|\delta\mathbf F_i\|}{\sigma_{\min}(\mathbf J_i)}.
\]

The same factor amplifies field and localization noise. Large motion is therefore not equivalent to improved parameter signal-to-noise ratio.

The correct quantity is the parameter information after noise propagation:

\[
\mathbf H^T\boldsymbol\Sigma_S^{-1}\mathbf H,
\]

not \(\|\mathbf H\|\) alone. A design that increases sensitivity and covariance by the same factor yields no information gain. Near bifurcation, the linear Gaussian approximation may fail completely and threshold-crossing statistics are required.

## 11. Mode Selectivity

Write a noise-whitened sensitivity matrix

\[
\widetilde{\mathbf H}=\boldsymbol\Sigma_S^{-1/2}\mathbf H
=\mathbf U_H\boldsymbol\Sigma_H\mathbf V_H^T.
\]

The right singular vectors are perturbation modes, the left singular vectors are feature-motion patterns, and singular values quantify noise-normalized observability.

Engineering singularity placement and local Jacobians may be useful if it:

- increases the smallest singular value for target modes;
- reduces the condition number over an admitted parameter domain;
- makes target and nuisance subspaces more orthogonal;
- produces sparse or interpretable left-singular patterns; or
- maintains these properties under calibration error.

For nuisance sensitivity \(\widetilde{\mathbf B}\), a possible design objective is

\[
\max_{\text{field design}}
\sigma_{\min}(\mathbf P_{\widetilde B}^{\perp}\widetilde{\mathbf H})
\]

subject to power, aperture, dynamic-range, feature-separation, and robustness constraints.

This is a plausible design program, not a demonstrated advantage. Ordinary full-field experiment design can optimize the same objective and remains the comparison baseline.

## 12. Topological Observables

### Metric information

Metric observables include position, normal displacement, velocity, trajectory curvature, inter-feature distance, and local Jacobian. They support continuous estimation but are sensitive to localization and association error.

### Topological information

Topological observables include charge, linking or knot class, births, annihilations, and reconnections. They may support:

- robust state labels under perturbations that preserve topology;
- threshold or fault detection;
- event classification;
- integrity checks based on charge-conservation rules; and
- coarse regime identification when metric coordinates drift.

Their limitations are substantial:

- discrete invariants are constant over wide parameter regions and can carry no local differential information there;
- topology events occur at bifurcations where local linearization fails;
- the same event can be caused by multiple perturbations;
- finite sampling can mistake unresolved motion for birth or death;
- events may be sparse, hysteretic, or dominated by nuisance changes; and
- quantitative inversion from event sequences may be non-unique.

Topology is therefore more plausible for classification, threshold sensing, and fault detection than for high-resolution continuous reconstruction unless combined with metric information.

## 13. Minimal Analytical Example

### 13.1 Locally identifiable translation

Consider the two-dimensional field

\[
\Psi(x,y;\boldsymbol\theta,c)
=c\left[(x-\theta_x)+i(y-\theta_y)\right],
\qquad c\in\mathbb C\setminus\{0\}.
\]

The unknown complex factor \(c\) represents common amplitude gain and phase. It does not change the zero. Taking \(c=1\) for the derivative calculation gives

\[
\mathbf F=
\begin{bmatrix}
x-\theta_x\\
y-\theta_y
\end{bmatrix},
\quad
\mathbf J=
\begin{bmatrix}
1&0\\
0&1
\end{bmatrix},
\quad
\mathbf K=
\begin{bmatrix}
-1&0\\
0&-1
\end{bmatrix}.
\]

The zero is \(\mathbf r=(\theta_x,\theta_y)\), and

\[
\delta\mathbf r=-\mathbf J^{-1}\mathbf K\delta\boldsymbol\theta
=\delta\boldsymbol\theta.
\]

The parameter is locally and globally identifiable from the labelled zero. This proves only that a singularity can encode translation, not that it is superior to the field samples used to locate it.

Within this restricted noiseless affine family, the two-coordinate zero is an exact invariant to the two-real-dimensional nuisance \(c\) and is sufficient to recover the two translation parameters. Relative to a dense sampled field, it is therefore a genuine low-dimensional task statistic. This establishes a narrow theoretical benefit under Gate criteria 1 and 2. It does not prove sufficiency after noisy field sampling, unknown additive background, model mismatch, or localization error; those conditions can reintroduce dependence on \(c\) and favour the complete field likelihood.

### 13.2 Apparent high sensitivity without information gain

Let

\[
\Psi_\varepsilon(x,y;\theta)
=\varepsilon x-\theta+i y,
\qquad \varepsilon>0.
\]

The zero is \(x=\theta/\varepsilon\), \(y=0\), with

\[
\mathbf J=
\begin{bmatrix}
\varepsilon&0\\
0&1
\end{bmatrix},
\qquad
\mathbf K=
\begin{bmatrix}
-1\\0
\end{bmatrix},
\qquad
\frac{\partial x}{\partial\theta}=\frac{1}{\varepsilon}.
\]

As \(\varepsilon\rightarrow0\), the singularity moves greatly for a small parameter change. But additive real-field residual noise with variance \(\sigma_F^2\) gives

\[
\operatorname{Var}(x)\approx\frac{\sigma_F^2}{\varepsilon^2}.
\]

Estimating \(\theta=\varepsilon x\) yields

\[
\operatorname{Var}(\widehat\theta)\approx\sigma_F^2,
\]

so the apparent displacement gain cancels the localization-noise gain. This is the simplest counterexample to “moves more, senses better.”

### 13.3 Multiple singularities but non-identifiable parameters

For known distinct anchors \((a_i,b_i)\), let

\[
\Psi_i(x,y;\theta_1,\theta_2)
=x-a_i-(\theta_1+\theta_2)+i(y-b_i).
\]

Every zero moves by

\[
\delta\mathbf r_i=
\begin{bmatrix}
1&1\\
0&0
\end{bmatrix}
\begin{bmatrix}
\delta\theta_1\\
\delta\theta_2
\end{bmatrix}.
\]

Stacking any number of such singularities does not raise \(\operatorname{rank}\mathbf H\) above one. Only \(\theta_1+\theta_2\) is identifiable. More singularities add precision for the same mode, not a new observable mode.

### 13.4 Global ambiguity of an unordered set

Let the complex coordinate be \(z=x+i y\) and

\[
\Psi(z;\theta)=z^2-\theta^2.
\]

The unordered zero set is

\[
S(\theta)=\{-\theta,+\theta\}=S(-\theta).
\]

Away from \(\theta=0\), a labelled branch may be locally trackable, but the unordered state cannot determine the sign globally. At \(\theta=0\), the double zero is degenerate and the local first-order model fails.

## 14. Failure Modes

1. **Generic 3D zeros are lines, not points.** A point-cloud state may be physically ill-defined.
2. **Rank deficiency.** Many features can respond to the same parameter combination.
3. **Poor conditioning.** Small singular values of the noise-whitened \(\mathbf H\) make inversion unstable.
4. **Noise amplification.** Near-singular spatial Jacobians amplify field residuals and localization error.
5. **Lossy extraction.** Positions discard amplitude, phase gradients, curvature, and nonzero-field structure.
6. **Association failure.** Permutations, crossings, missed detections, births, and deaths corrupt trajectories.
7. **Symmetry ambiguity.** Different perturbations can produce identical unordered sets.
8. **Bifurcation failure.** Linearization is invalid at creation, annihilation, splitting, and reconnection.
9. **Correlated errors.** Treating shared field-reconstruction noise as independent feature noise inflates apparent information.
10. **Dark-core localization.** Zero intensity can reduce photon information at precisely the feature being localized.
11. **Model mismatch.** An engineered basis may be selective only for assumed perturbations and blind to unmodelled ones.
12. **Baseline weakness.** Beating an inefficient full-field algorithm does not show information or sensing superiority.
13. **Calibration burden.** Estimating \(\mathbf J_i\), \(\mathbf K_i\), and feature identities may cost as much as field reconstruction.
14. **Dynamic-range and topology tradeoff.** Designs near a topology transition may be responsive but fragile and narrow-range.

## 15. What the Representation Cannot Do

The singularity state cannot:

- create information absent from the measurement channel;
- exceed an optimal estimator using the same complete field data;
- make an unidentifiable perturbation identifiable unless the field design or measurement channel changes;
- recover amplitude and phase information discarded by position-only extraction;
- guarantee noise robustness merely because zeros or charges are topological;
- turn a large coordinate response into improved parameter signal-to-noise ratio automatically;
- make generic 3D scalar-field zeros into stable isolated points;
- replace a nuisance and calibration model; or
- support broad cross-domain claims without domain-specific forward and noise models.

## 16. Theory Gate Verdict

**CONDITIONAL PASS**

Local identifiability is achievable for restricted perturbation models when the represented feature coordinates are well defined and the noise-weighted global sensitivity matrix has full column rank. In the explicit affine translation family, the zero coordinate is an exact noiseless sufficient statistic for translation and is invariant to unknown nonzero complex gain. This is a defensible but narrow dimensional-reduction and nuisance-invariance result under Gate criteria 1 and 2.

The gate does not pass unconditionally because no general information advantage exists. If the singularity state is derived from the same complete field data, it cannot exceed full-field Fisher information. Large motion can be cancelled exactly by amplified localization noise, and a 3D point-state model is generically invalid for scalar fields whose zeros form lines.

A practical advantage remains plausible only for a narrow problem where at least one of the following is demonstrated:

- near-sufficient compression with quantified information retention;
- invariance to realistic nuisance gain or phase variables;
- a well-conditioned mode-selective field design;
- useful topology-based classification or fault detection; or
- direct feature acquisition that avoids full-field reconstruction cost.

This is enough to justify one bounded numerical gate, but not a theory paper or broad application program.

## 17. Required Next Work

Proceed only to a minimal, falsifiable numerical evaluation:

1. Select a two-dimensional optical scalar-field testbed first. This avoids hiding the generic 3D line-state problem.
2. Use a small parameter vector containing one target mode and at least one nuisance mode.
3. Define the actual detector samples and noise model before extracting singularities.
4. Compute the full-field efficient Fisher information and the singularity-state Fisher information from the same samples.
5. Measure the information-retention ratio, condition number, estimator error, and data/computation reduction.
6. Include adversarial perturbations in the null space or near-null space of \(\mathbf H\).
7. Include common gain, common phase, relative source-phase drift, additive detector noise, calibration error, missed features, and label swaps.
8. Compare positions alone against positions plus charge and local Jacobian.
9. Reject the architecture for the selected problem if it provides only larger motion without information retention, invariance, conditioning, or material practical savings.
10. Address 3D only after defining a vortex-line or landmark representation and its gauge.

No numerical simulation was performed, no experimental result is claimed, and no theory paper has been written.
