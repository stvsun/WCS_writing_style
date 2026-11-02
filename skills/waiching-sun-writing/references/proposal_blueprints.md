# Research Grant Proposal & White Paper Blueprints (DoD, NSF, DOE)

This guide defines Prof. WaiChing Sun's structural, persuasive, and technical framing conventions for research proposals across **DoD Basic Research (ARO, AFOSR, ONR)**, **NSF (CMMI, OAC, CAREER)**, and **DOE (ASCR, BES)**.

---

## 1. Core Proposal Philosophy (How Proposals Differ from Journal Papers)

Whereas a journal article reports a *completed* mathematical and computational closure, a proposal must establish:
1. **Why Now & Why This Formulation**: A sharp conceptual distinction between **incremental engineering workarounds** (what everyone else is doing) and the **foundational mathematical/mechanistic reformulation** proposed by the PI.
2. **Hypothesis-Driven Architecture**: Every Research Thrust (or Task) is anchored by an explicit, falsifiable **Scientific Hypothesis** paired with a **Mathematical/Computational Mechanism** and a **Verification/Validation Metric**.
3. **Closed-Loop Interdependence Across Thrusts**: Thrusts must never read like three independent mini-projects stapled together. Explicitly articulate the mathematical objects passed from Thrust 1 $\to$ Thrust 2 $\to$ Thrust 3 and the feedback loop back to Thrust 1.

---

## 2. DoD Basic Research Blueprints (ARO, AFOSR, ONR)

### A. DoD White Paper (3–5 Pages)
DoD Program Managers read white papers to assess (1) fundamental 6.1 basic research novelty, (2) alignment with program priorities, and (3) Heilmeier Catechism clarity.

**Structure**:
1. **Objective & Scientific Vision (0.5 page)**:
   - Open with a bold, single-sentence statement of the fundamental scientific goal.
   - Immediately answer: *What is the fundamental physics/mathematics barrier preventing current mechanics/SciML models from succeeding in extreme defense-relevant regimes (e.g., high-strain-rate granular/porous impact, shock-induced phase transition, sparse/noisy multi-fidelity data)?*
2. **State of the Art & Its Structural Limitations (0.75 page)**:
   - Contrast current paradigms cleanly (often summarized in a high-density comparison table or conceptual schematic).
3. **Overarching Hypothesis & Technical Approach (2–2.5 pages)**:
   - State the **Central Hypothesis** in bold or italic block formatting.
   - Organize into **2–3 tightly coupled Research Thrusts**:
     - *Thrust 1*: Theoretical / Mathematical Foundation (e.g., geometric/thermodynamic formulation, Lie-algebraic invariance, operator theory).
     - *Thrust 2*: Algorithmic / Scientific Machine Learning Realization (e.g., structure-preserving neural operators, game-theoretic active learning, uncertainty quantification).
     - *Thrust 3*: Multiscale Verification, Extreme-Regime Validation & Stability Analysis.
4. **DoD / Army / Air Force / Navy Relevance & Payoff (0.5 page)**:
   - Connect the fundamental 6.1 breakthroughs to concrete long-term DoD capabilities (e.g., penetration mechanics in earth/concrete penetrators, terrestrial mobility on multiphase terrains, resilient architected armor/metamaterials, autonomous digital twins).

### B. Implicit Heilmeier Check (Mandatory in All DoD Drafts)
Ensure the opening 1.5 pages answer all Heilmeier questions without sounding like a mechanical questionnaire:
- *What are you trying to do?* (Zero jargon summary alongside exact mathematical goal)
- *How is it done today, and what are the limits of current practice?*
- *What is new in your approach and why do you think it will be successful?*
- *If you are successful, what difference will it make?*
- *What are the risks, and what are the mid-term and final "exams" to check for success?*

---

## 3. NSF Proposal Blueprints (CMMI, OAC, CAREER)

### A. Project Summary (Strict 1-Page Structure)
Must contain three explicitly titled, self-contained sections:
1. **Overview**:
   - Paragraph 1: Physical/engineering problem and fundamental scientific bottleneck.
   - Paragraph 2: Overarching goal, central hypothesis, and the three integrated Research Thrusts.
2. **Intellectual Merit**:
   - Specify the theoretical advances in continuum mechanics/poromechanics, applied mathematics, and/or scientific machine learning, and how they generalize beyond a single material system.
3. **Broader Impacts**:
   - Societal/engineering impact (e.g., geologic carbon storage safety, infrastructure resilience, open-source software dissemination) integrated with educational curriculum innovation and mentoring at Columbia University.

### B. Project Description (15 Pages)
1. **Section 1 — Vision, Motivation, and Fundamental Knowledge Gaps (2.5–3 pages)**:
   - Establish why current mechanics + ML approaches fail when extrapolating across scales, loading regimes, or microstructural topologies.
   - Include a high-level **Framework Overview Diagram** mapping the bidirectional coupling among Thrusts 1, 2, and 3.
2. **Section 2 — Results from Prior NSF Support (if applicable, 0.5–1 page)**:
   - Award number, title, period, specific intellectual achievements, publications produced, and **how the proposed work builds upon yet departs fundamentally from prior work**.
3. **Section 3 — Research Plan (8.5–9.5 pages)**:
   - For each **Thrust $i$ ($i=1,2,3$)**:
     - **Research Question & Hypothesis $i$**
     - **Mathematical Formulation & Technical Tasks ($i.1, i.2, \dots$)** (Include concrete governing equations, functional spaces, or loss functionals—never write equation-free hand-waving in an NSF mechanics proposal!)
     - **Verification Benchmarks, Success Metrics & Potential Pitfalls / Alternative Strategies**
4. **Section 4 — Broader Impacts & Integration of Research and Education (1.5–2 pages)**:
   - Open-source software release plan, Columbia University course modules (e.g., computational poromechanics, tensor mechanics, SciML for mechanics), and undergraduate/graduate research training.
5. **Section 5 — Management Plan & Timeline (0.5 page)**:
   - Year-by-year Gantt/milestone matrix across all Thrusts and personnel.

---

## 4. DOE Proposal Blueprints (ASCR / BES)

- **ASCR (Applied Mathematics / Scientific Machine Learning)**:
  - Lead with **mathematical rigor**: approximation theory, stability, structure preservation (symplectic/thermodynamic/Lie-group structure), error bounds, and scalability to high-dimensional PDEs.
  - Motivate with complex multiphysics mechanics applications as the proving ground.
- **BES (Geosciences / Materials Sciences)**:
  - Lead with **multiscale physical mechanisms** in porous/fractured geological media or complex materials (thermo-hydro-mechanical-chemical coupling, mineral dissolution/precipitation, sub-grid fracture propagation).
  - Frame mathematical/SciML innovations as the rigorous bridge connecting pore-scale physics (synchrotron X-ray $\mu$CT, molecular/grain scale) to continuum field-scale behavior.
