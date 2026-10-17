# Nova Continuity

## Project / objective

Maintain a public-facing archive for Carson's engineering concepts, theory work, simulations, prototypes, diagrams, and papers.

## Repository state

- Branch `main` tracks `origin/main` at published baseline `a199d1a49c4e0bb5203df3b7fd2c686e79921a8a`, `Update continuity after Simulation Gate 3 publication`; divergence is `0/0`. The worktree contains only the uncommitted Theory Gate 2 report and required bookkeeping updates, and the index is clean.
- The novelty review and Theory Gate 1 are published and verified.
- Simulation Gate 1 is published and verified with verdict **HOLD** at the synchronized baseline `54f371a357039ad492dfda9b691b62e481ee5644`.
- Simulation Gate 1B is published and verified with verdict **PASS**, narrowly for the bounded translation information-ceiling question. The worktree and index are clean, with `main` and `origin/main` at `0/0` divergence.
- Simulation Gate 2 is published and verified with verdict **FAIL** for the tested local compact singularity-centered architecture in the bounded four-parameter 2D task. The worktree and index are clean, with `main` and `origin/main` at `0/0` divergence.
- Simulation Gate 3 is published and verified with verdict **FAIL** for the tested distributed product-field singularity-coordinate network in the bounded four-parameter 2D task.

## Current objective

Theory Gate 2 has been performed locally and awaits Carson's review. Verdict: **CONDITIONAL PASS**. Golden-ratio spacing sub-verdict: **NO SPECIAL ADVANTAGE FOUND**.

## Current state

- Root repository guidance and concept index are present.
- The first concept, `3D Singularity Sensing Lattice`, has placeholder documentation and workspace directories.
- A reusable concept template is present under `shared/templates/concept-template/`.
- `concepts/singularity-sensing-lattice/novelty-review.md` records a skeptical prior-art review.
- `REFERENCES.md`, `STATUS.md`, and `ASSUMPTIONS.md` reflect the review; `notes/terminology-map.md` maps adjacent terminology.
- `concepts/singularity-sensing-lattice/theory-gate-1.md` records the information, identifiability, Fisher-information, noise, and conditioning analysis.
- `simulation-gate-1.md`, `simulations/simulation_gate_1.py`, generated result data, and generated figures record a matched-data 2D translation comparison.
- `simulation-gate-1b.md`, `simulations/simulation_gate_1b.py`, generated result data, and generated figures decompose the translation-information ceiling from extractor loss.
- `simulation-gate-2.md`, `simulations/simulation_gate_2.py`, generated result data, and generated figures test a four-parameter multi-mode family and a hierarchy of local compact states.
- `simulation-gate-3.md`, `simulations/simulation_gate_3.py`, generated result data, and four generated figures test a distributed product-field singularity-coordinate network.
- `theory-gate-2.md` derives singularity-anchored nonlocal modal summaries for the Gate 2 analytical field. No new simulation was run.

## Authorities / constraints / invariants

- Git and authoritative project artifacts are the source of truth.
- Do not commit, push, publish, delete, or configure a remote without Carson's explicit authorization.
- Distinguish hypotheses and speculation from demonstrated results.
- Do not fabricate references or overstate experimental evidence.

## Validation state

- Exact expected file inventory verified.
- Text files verified as UTF-8 without BOM, with LF endings and final newlines.
- Initial commit and publication were previously verified.
- Novelty review and Theory Gate 1 publication, commit identity, clean state, and remote synchronization were verified at `1969540f6ee71f9f93a6a8697d4782e42b220bbc`.
- Simulation Gate 1 ran 2,880 fixed-seed trials across 40, 30, 20, and 10 dB SNR and nine complex-gain settings per SNR.
- Internal checks passed for zero location, gain invariance, Fisher symmetry, Fisher positive semidefiniteness, and estimator sanity.
- Simulation Gate 1 verdict: **HOLD**.
- Simulation Gate 1 publication, commit identity, clean state, and remote synchronization were verified at `ab864e5eddde90675588ea95544b19afbb3977e4`.
- Simulation Gate 1B used the exact Gate 1 model, 5,760 main paired trials, and a bounded 21x21/31x31/41x41 grid and 3x3/5x5/7x7 window study.
- Simulation Gate 1B verdict: **PASS** for the narrow translation information-ceiling question.
- Simulation Gate 1B publication, commit identity, clean state, and remote synchronization were verified at `4502de440d75753e21e9a0b572742284c817b931`.
- Simulation Gate 2 used baseline `f6106b5e75396646f88eaa9ebd10a31943fcaddc`, parameters `[dx,dy,alpha,beta]`, 2,400 paired trials, and state dimensions 2, 6, 14, 50, and 1,922.
- Gate 2 verdict: **FAIL**. The best tested state with at most 20 values was S14 at 8.84% joint retention; its weakest parameter retained about 0.01%.
- Simulation Gate 2 publication, commit identity, clean state, and remote synchronization were verified at `321c696a15c86faef83cddc736e4bee07660bfbd`, `Complete Simulation Gate 2 multi-mode compact-state analysis`.
- Simulation Gate 3 used baseline `19c1822e5e44c4d7255e2ce94cd0d769f098a919`, parameters `[dx,dy,alpha,beta]`, singularity counts 1, 2, 4, 8, and 16, three placement strategies, and 36,000 paired trials.
- Gate 3 verdict: **FAIL** for the tested distributed product-field singularity-coordinate network. The best configuration was optimized placement at N=1, with 15.98% practical joint retention, 17.43% ideal coordinate retention, and 1.21% worst required-parameter retention.
- Optimized tracking failure reached 77.29% at N=8 and 99.92% at N=16. Placement affected small-network response and tested global-gain invariance held, but additional singularities did not improve useful relative information. The ideal coordinate ceiling was already weak, and extraction was not the only bottleneck.
- Simulation Gate 3 publication, commit identity, clean state, and remote synchronization were verified at `eb98c1cd1ce7981961681377c9d2e79ee97ab84c`, `Complete Simulation Gate 3 distributed network analysis`.
- Theory Gate 2 baseline: `a199d1a49c4e0bb5203df3b7fd2c686e79921a8a`.
- Field family: translated charge-one Gaussian-envelope vortex with anisotropy `alpha`, radial phase curvature `beta`, and unknown nonzero global complex gain.
- Derived couplings: zero position carries `[dx,dy]`; the `m=3/m=1` harmonic ratio carries `alpha`; cross-shell `m=1` phase slope carries `beta`.
- Minimal candidate state: four real values. Its nominal sensitivity matrix is `diag(1,1,-rho_a/4,1)`, full rank for every admitted `r_a>0`.
- Conditioning result: algebraic scaling can be balanced, but noise-weighted conditioning and retained information remain unverified.
- Centering result: complete circular odd-harmonic summaries reject first-order centering leakage at the nominal point by parity; practical and higher-order sensitivity remain unresolved.
- Theory Gate 2 verdict: **CONDITIONAL PASS**. Golden-ratio sub-verdict: **NO SPECIAL ADVANTAGE FOUND**.

## Open issues / risks

- License has not been selected.
- Novelty verdict: **CONDITIONAL GO** at the architecture level, not a novelty or patentability claim.
- Closest threats are optical-vortex metrology, singularity-network displacement measurement, optical rulers, engineered point arrays, and 3D nodal topology.
- The decisive unresolved question is whether the singularity state provides a measurable information, robustness, compression, or computational advantage over the same underlying full-field data.
- Theory Gate 1 verdict: **CONDITIONAL PASS**.
- Strongest positive result: local identifiability is achievable for restricted models when the defined feature coordinates yield a full-column-rank, noise-weighted sensitivity matrix.
- Strongest failure risk: a state extracted from the same complete field cannot exceed full-field information, while near-singular spatial Jacobians amplify localization noise and generic 3D scalar-field zeros form lines rather than isolated points.
- Gate 2 locality result: the normalized 5x5 patch retained 7.70% joint information, classifying global field context as necessary for the admitted deformation modes.
- Gate 2 timing result: the implemented compact pipeline showed no total-pipeline computational advantage over the local full-field GLS benchmark, and no local acquisition advantage was demonstrated.
- Further mathematical framework, simulation, and experimental validation remain pending.
- Theory Gate 1 itself contained no numerical simulation; Simulation Gate 1 now supplies bounded 2D numerical evidence. No theory paper has been written.
- Strongest Simulation Gate 1 positive result: the two-coordinate state was exactly common-gain invariant in the noiseless model, compressed 1,922 real samples to 2 post-extraction values, and required about one thirteenth of the estimator runtime in the authoritative recorded invocation.
- Strongest Simulation Gate 1 negative result: the tested extractor retained about 14% of full-field efficient Fisher information on average, with materially higher RMSE, and was blind to an exact zero-preserving deformation.
- Practical advantage remains plausible only if improved extraction, direct feature acquisition, or a nonredundant multi-feature state can meet a predefined retention and cost target.
- No 3D simulation or experiment was performed, and no paper was written.
- Ideal zero-state translation retention is 100%; profile coordinate localization reached that ceiling within Monte Carlo error.
- The published approximately 14% Gate 1 result is primarily an affine-extractor limitation for this exact task; representation loss is 0% for translation and approximately 86% of information was lost by the Gate 1 extractor.
- Strongest positive result: a two-coordinate output can preserve essentially all matched translation information while retaining ideal global-gain invariance.
- Strongest negative result: efficient profile extraction uses the complete field likelihood, provides no demonstrated acquisition or compute reduction, and the coordinate state remains blind to zero-preserving deformation.
- The principal Gate 1 bottleneck is extraction, not representation, for the bounded translation model.
- Strongest Gate 2 positive result: a deterministic 14-value gain-invariant descriptor was measurable without extraction failures.
- Strongest Gate 2 negative result: that descriptor retained only 8.84% joint information and effectively lost the zero-preserving modes.
- Gate 2's **FAIL** is limited to the tested local compact architecture and does not extend automatically to distributed or multi-singularity architectures.
- No 3D simulation or experiment was performed, no hardware was designed, and no paper was written.
- Gate 3 baseline: `19c1822e5e44c4d7255e2ce94cd0d769f098a919`; counts 1, 2, 4, 8, 16; placements naive, diverse, optimized; 36,000 paired trials.
- Best result: optimized N=1, 15.98% practical joint retention, 1.21% worst-mode retention, dimension 2, and 961x post-extraction reduction.
- Strongest positive result: placement changed small-N response and gain invariance held.
- Strongest negative result: count did not improve retention and tracking failure became severe for crowded networks.
- Direct distributed coordinate-feature acquisition is not justified by the Gate 3 result.
- The present compact singularity-coordinate architecture line is no longer supported for the broader multi-mode task: Gate 2 rejected the tested local compact single-singularity states, and Gate 3 rejected the tested distributed product-field coordinate network.
- Any further research must materially change the retained statistic or field architecture rather than merely refine the failed coordinate-network line.
- Gate 3's **FAIL** does not automatically extend to all distributed sensing architectures, all multi-singularity field architectures, non-coordinate distributed statistics, singularity-anchored multiscale sampling, or alternative sparse nonlocal summaries.
- No 3D work, experiment, hardware design, or paper drafting occurred for Gate 3.
- Strongest Theory Gate 2 positive result: a gain-invariant four-real-value state is explicitly defined and locally full rank, with translation, anisotropy, and radial phase curvature separated into distinct channels.
- Strongest Theory Gate 2 negative result: useful noise-weighted conditioning and information retention are not established, and the beta channel is phase wrapped without an admitted bound or unwrapping rule.
- The singularity can serve as an analytical reference origin even though coordinate-only states failed. Nonlocal deformation sensitivity grows as `r^2` relative to the field near the zero, explaining the local-state failure and motivating shell summaries.
- No special analytical advantage was found for golden-ratio spacing. Optimized radii require an explicit noise model and objective.
- No new simulation, 3D work, experiment, hardware design, or paper drafting occurred for Theory Gate 2. No commit or push occurred.

## Ordered next actions

1. Carson reviews the Theory Gate 2 derivation and its **CONDITIONAL PASS** verdict.
2. If separately authorized, define a bounded 2D simulation comparing the four-value state and small redundant variants against the efficient full-field benchmark.
3. Predefine radius bounds, angular sampling, denominator floors, beta phase range, centering perturbations, summary covariance, and one common spacing-selection criterion.
4. Compare uniform, ordinary geometric, golden-ratio, and optimized radii without assuming a golden-ratio advantage.
5. Do not begin simulation, 3D work, experiment, hardware design, or paper drafting without separate authorization.
6. Commit or push only with explicit authorization.
