# Assumptions

Status labels describe the literature evidence reviewed on 2026-10-14. They do not establish feasibility for the proposed architecture.

## Established in related systems

- **Phase singularities can be deliberately generated and spatially arranged.** Optical metasurface experiments have produced point arrays and sheet structures.
- **Phase singularities can be localized with useful precision in specific optical systems.** Published displacement-metrology demonstrations range from nanometric to picometric-scale localization claims under controlled conditions.
- **Perturbations can measurably displace or deform singularities.** Displacement, aberration, propagation, and refractive-index perturbations have documented effects.
- **Multiple singularities can be detected and matched.** Optical-vortex metrology, singularity-network methods, and patent literature demonstrate this in two-dimensional image-derived representations.
- **Common nonzero complex scaling leaves exact field zeros unchanged.** This gives invariance to ideal global amplitude gain and common phase, although it does not cover additive offsets, saturation, relative source-phase drift, or reconstruction error.

These established statements are limited to the cited systems and do not establish a general 3D distributed sensor.

## Plausible but system-dependent

- **Coherent or sufficiently phase-stable sources are available.** Plausible in optical and RF laboratory systems, but stability requirements scale with aperture, duration, bandwidth, and desired localization accuracy.
- **The underlying complex field can be measured or reconstructed.** Established techniques exist, but volumetric coverage, calibration, bandwidth, and detector access may make the proposed geometry impractical.
- **Engineered local field gradients can shape sensitivity.** Prior work inverse-designs phase gradients and singularity morphology, but mode-selective sensor design remains to be demonstrated.

## Unverified critical assumptions

- **A large 3D singularity population can be generated, observed, and tracked simultaneously at useful rates and signal-to-noise ratio.**
- **A perturbation field is identifiable from the singularity state.** Distinct perturbations may produce indistinguishable zero sets.
- **Birth, annihilation, and reconnection events can be associated reliably rather than causing catastrophic tracking ambiguity.**
- **Useful signal can be separated from source, environmental, detector, and calibration noise using collective correlations.**
- **The singularity representation preserves enough task-relevant information for inverse reconstruction.**
- **Collective singularity behavior provides a measurable advantage over optimal estimators using the same full-field data.** This is the decisive unverified assumption.
- **The noise-weighted global sensitivity matrix has full column rank and acceptable conditioning over the admitted operating region.** More singularities do not guarantee more observable parameter modes.
- **The chosen 3D feature coordinates are intrinsic and reproducible.** Generic scalar-field zeros in 3D are curves, so point labels require cross-sections, landmarks, additional constraints, or a defined gauge.
- **Feature-localization and association errors can be modelled without materially overstating Fisher information.** Shared field noise will generally correlate errors across singularities.
- **The architecture transfers from optics to RF, acoustics, strain, or environmental sensing without losing its proposed advantages.**

## Contradicted or requiring reformulation

- **A generic three-dimensional scalar field supports a stable lattice of isolated point singularities.** This is not generally true. Generic complex scalar-field zeros in 3D form lines; isolated points or sheets require extra constraints, symmetry, approximation, or active engineering and may unfold under perturbation.
- **High local phase gradient alone guarantees improved sensitivity or signal-to-noise ratio.** Prior sensing literature, including exceptional-point analyses, shows that enhanced response can be offset by reduced signal, noise, or instability. Sensitivity must be evaluated with a complete measurement and noise model.
- **A singularity statistic derived from a complete field measurement can contain more information than that field measurement.** Under the same likelihood and regularity conditions, data processing forbids this. Any defensible advantage must be compression, nuisance invariance, conditioning for a restricted task, practical measurement efficiency, or direct feature acquisition.
- **Adding more singularities necessarily improves identifiability.** Repeated sensitivity rows add redundancy but not rank; correlated localization errors can further reduce the practical gain.
