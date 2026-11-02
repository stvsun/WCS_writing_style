# Journal Manuscript Structural Blueprints

This reference codifies the section-by-section rhetorical architecture for Prof. WaiChing Sun's journal articles across:
- **Computational Mechanics & Solids Journals**: *Computer Methods in Applied Mechanics and Engineering (CMAME)*, *Journal of the Mechanics and Physics of Solids (JMPS)*, *International Journal for Numerical Methods in Engineering (IJNME)*, *Journal of Computational Physics (JCP)*.
- **Geomechanics & Poromechanics Journals**: *International Journal for Numerical and Analytical Methods in Geomechanics (IJNAMG)*, *Acta Geotechnica*, *Water Resources Research (WRR)*, *Computers and Geotechnics*.

---

## 1. Abstract Blueprint (The 4-Move High-Density Structure)

Target length: **160–240 words** in a single cohesive paragraph. Never use vague promises (*"Results will be discussed"*).

1. **Move 1 — Context & Fundamental Bottleneck (1–2 sentences)**:
   Identify the physical system (e.g., fluid-infiltrated porous media, history-dependent elastoplastic solids, architected metamaterials) and pinpoint why existing modeling paradigms fail (e.g., loss of thermodynamic admissibility, prohibitive cost of nested $\text{FE}^2$ homogenization, coordinate-system dependence).
2. **Move 2 — Proposed Theoretical/Computational Framework (2–3 sentences)**:
   State what is formulated (*"In this work, we introduce/formulate..."*). Specify the exact mathematical foundation (e.g., Lie-group representation, variational phase-field operator split, thermodynamics-informed neural network with Sobolev training, multi-agent reinforcement learning game).
3. **Move 3 — Theoretical Guarantees & Algorithmic Mechanism (1–2 sentences)**:
   State what properties are preserved *by construction* (e.g., material frame indifference, non-negative internal dissipation, inf-sup stability, mesh objectivity).
4. **Move 4 — Verification & Validation Payoff (1–2 sentences)**:
   Summarize the verification benchmarks and boundary-value problems solved, highlighting quantitative gains in accuracy, stability, or speedup.

---

## 2. Introduction Blueprint (The 5-Stage Funnel)

Target length: **6–10 paragraphs** (~1,000–1,600 words).

1. **Stage 1 — Physical Motivation & Engineering Significance (Paragraphs 1–2)**:
   Open with the physical phenomenon and engineering/geophysical applications (e.g., fault reactivation, subsurface $\text{CO}_2$ sequestration, hydraulic fracturing, impact-resistant metamaterials). Explain why multiphysics or multiscale coupling governs the macroscopic response.
2. **Stage 2 — Critical Taxonomy of Existing Approaches (Paragraphs 3–5)**:
   Group the literature into **conceptual schools of thought** rather than a chronological list:
   - *School A* (e.g., classical phenomenological constitutive models): fast and interpretable, but rely on predefined yield/potential surfaces and struggle with complex microstructural evolution.
   - *School B* (e.g., direct multiscale homogenization such as $\text{FE}\times\text{FE}$ or $\text{FE}\times\text{DEM}$): physically faithful, but computationally intractable for large-scale 3D boundary-value problems.
   - *School C* (e.g., black-box data-driven surrogates): fast at inference, but often violate frame indifference, thermodynamic constraints, or lose ellipticity inside nonlinear PDE solvers.
3. **Stage 3 — The Exact Knowledge Gap (Paragraph 6)**:
   Synthesize the tension between Schools A, B, and C into a sharp technical statement of what is missing.
4. **Stage 4 — Proposed Approach & Core Contributions (Paragraphs 7–8)**:
   Begin with *"To overcome these limitations, we propose..."* or *"In this study, we introduce..."*. Clearly enumerate the 3–4 main contributions (either in a tight prose sequence or an itemized list when writing for *CMAME* / *IJNME*).
5. **Stage 5 — Roadmap & Notation Paragraph (Final 1–2 Paragraphs)**:
   - Organization roadmap: *"The remainder of this paper is organized as follows. Section 2 presents... Section 3 details... Section 4 provides verification and numerical examples... Finally, Section 5 summarizes the main conclusions."*
   - Standard tensor notation paragraph (see `math_and_mechanics_notation.md`).

---

## 3. Formulation & Methodology Sections (Sections 2–3)

Divide theoretical formulation cleanly from numerical/ML implementation:
- **Section 2 (Governing Equations / Constitutive Theory)**:
  - Kinematics and geometric configuration first.
  - Balance laws (mass, momentum, energy) and entropy inequality (Clausius–Duhem inequality).
  - Constitutive assumptions and thermodynamic conjugate pairs derived systematically.
  - Use `\begin{remark}` blocks to contrast the formulation against simplified classical theories.
- **Section 3 (Discretization / Operator Split / Learning Architecture)**:
  - Weak form, function spaces, and stability considerations (e.g., LBB condition for mixed $u$-$p$ poromechanics).
  - Or, for SciML papers: architecture design, geometric invariants used as inputs, Sobolev loss functional definition, training data generation / active learning loop, and consistent tangent derivation via automatic differentiation for finite element integration.
  - Include a self-contained `\begin{algorithm}` block summarizing the offline training or online return-mapping / time-stepping loop.

---

## 4. Numerical Examples & Verification Section (Section 4)

Always order numerical examples from **rigorous verification** to **complex capability demonstration**:
1. **Example 1 — Analytical / Benchmark Verification**:
   - Material-point or simple boundary-value problem with a known analytical or high-fidelity reference solution (e.g., 1D Terzaghi consolidation, simple shear / pure dilation symmetry test, manufactured solution).
   - Purpose: Verify convergence rate, frame invariance under rigid-body rotation, or thermodynamic dissipation non-negativity.
2. **Example 2 — Ablation / Sensitivity / Extrapolation Study**:
   - Compare the proposed framework against baseline alternatives (e.g., unconstrained MLP vs. thermodynamics-informed architecture, or $L_2$ vs. $H^1$ Sobolev training) under unseen loading paths or cyclic loading-unloading.
3. **Example 3 — Complex 2D/3D Boundary-Value Problem or Experimental Validation**:
   - Demonstrate performance inside a full finite element solver (e.g., strain localization in a fluid-saturated specimen, perforated metamaterial plate, triaxial compression of digital rock).
   - **Prose Rule for Interpreting Plots**: Never write *"Figure 5 shows that the red line is close to the black dots."* Instead, write: *"As shown in Fig. 5, enforcing polyconvexity of the learned stored energy functional prevents spurious loss of ellipticity during softening, enabling the Newton–Raphson solver to converge quadratically past the peak load where unconstrained surrogates diverge."*

---

## 5. Conclusion Blueprint (Section 5)

Target length: **2–4 paragraphs**.
1. **Paragraph 1 (Synthesis)**: Restate the core theoretical and computational framework developed and the fundamental mechanics/SciML bottleneck it resolves.
2. **Paragraph 2 (Key Findings)**: Summarize the quantitative findings from the numerical experiments (what was verified, why the mechanism succeeded).
3. **Paragraph 3 (Candid Limitations & Future Directions)**: Explicitly identify current simplifying assumptions (e.g., small-strain kinematics, isothermal assumption, rate-independence) and state concrete extensions in progress.
