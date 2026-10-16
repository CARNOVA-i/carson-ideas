# Nova Continuity

## Project / objective

Maintain a public-facing archive for Carson's engineering concepts, theory work, simulations, prototypes, diagrams, and papers.

## Repository state

- Branch `main` tracks `origin/main` at commit `321c696a15c86faef83cddc736e4bee07660bfbd`, `Complete Simulation Gate 2 multi-mode compact-state analysis`.
- The novelty review and Theory Gate 1 are published and verified.
- Simulation Gate 1 is published and verified with verdict **HOLD** at the synchronized baseline `54f371a357039ad492dfda9b691b62e481ee5644`.
- Simulation Gate 1B is published and verified with verdict **PASS**, narrowly for the bounded translation information-ceiling question. The worktree and index are clean, with `main` and `origin/main` at `0/0` divergence.
- Simulation Gate 2 is published and verified with verdict **FAIL** for the tested local compact singularity-centered architecture in the bounded four-parameter 2D task. The worktree and index are clean, with `main` and `origin/main` at `0/0` divergence.

## Current objective

The next planned research question is Simulation Gate 3: Distributed Singularity Network. It has not started and requires separate Carson authorization.

At high level, Gate 3 would test whether multiple spatially separated singularities, treated collectively as a distributed state, can recover the multi-mode information that local single-singularity descriptors failed to preserve.

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
- Simulation Gate 3 has not started.

## Ordered next actions

1. Await Carson's authorization for Simulation Gate 3: Distributed Singularity Network.
2. If authorized, define a bounded 2D multi-singularity field architecture.
3. Test whether collective singularity displacement/state recovers zero-moving and zero-preserving modes.
4. Compare information retention versus singularity count and placement.
5. Do not begin 3D work, experiment, hardware design, or paper drafting without separate authorization.
6. Commit or push only with explicit authorization.
