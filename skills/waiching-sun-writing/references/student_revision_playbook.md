# Co-Author & Student Draft Revision Playbook

When Prof. WaiChing Sun revises a student's or co-author's manuscript or proposal draft, the goal is **not** cosmetic copy-editing. It is a structural and intellectual elevation that transforms lab-notebook narration or generic prose into authoritative computational mechanics scholarship while strictly preserving the underlying technical facts and numerical results.

---

## 1. The 4-Step Revision Protocol

Whenever asked to revise, edit, or rewrite a student/co-author draft:

1. **Step 1 — Diagnose Structural & Mechanistic Flaws**:
   Before rewriting, identify which of the 6 Common Student Draft Failure Modes (below) are present.
2. **Step 2 — Reorganize Paragraph & Equation Architecture**:
   - Re-order paragraphs so every paragraph starts with a physical, mathematical, or algorithmic premise (rather than a chronological action or a figure number).
   - Ensure every equation is grammatically integrated into a sentence and all symbols are defined with precise tensor order and physical meaning.
3. **Step 3 — Rewrite in Prof. Sun's Voice & Run Linter**:
   - Replace vague descriptors, conversational transitions, and AI clichés with precise continuum mechanics and applied mathematics terminology.
   - Run `style_linter.py` on the revised draft to verify zero errors.
4. **Step 4 — Provide a Concise Revision Summary**:
   - Present a short bulleted summary of the key structural and terminological upgrades made so the student/co-author learns from the edits.

---

## 2. Six Common Student Draft Failure Modes & How to Fix Them

### Failure Mode 1: "Plot Narration" Instead of Mechanistic Interpretation
- **Student Draft Symptom**: Describing colors, lines, and visual trends without explaining the governing physics or numerical mechanism.
- **Before (Student Draft)**:
  > *"Figure 6 shows the stress-strain curve for the drainage test. Looking at Fig. 6, the blue curve goes up and then drops quickly after the peak, while the red curve stays stable and converges to the reference solution. This shows our Sobolev training method is much better than standard MSE loss."*
- **After (Prof. WaiChing Sun Style — Concise Two-Sentence Cadence)**:
  > *"Figure 6 compares the drained triaxial stress–strain responses predicted by $L_2$-trained and $H^1$-trained neural surrogates. Both models capture the initial elastic response. Beyond the peak stress, however, the $L_2$ surrogate exhibits spurious stress oscillations because its unregularized tangent moduli cause the global Newton–Raphson solver to diverge. By contrast, $H^1$ Sobolev training supervises the stress derivatives directly, preserving acoustic-tensor ellipticity and reproducing the post-peak softening benchmark."*

---

### Failure Mode 2: "Annotated Bibliography" Literature Review
- **Student Draft Symptom**: A string of chronological paragraphs starting with *"Author et al. (2019) proposed X. Author et al. (2021) used Y. Recently, Author et al. (2023) studied Z."*
- **Before (Student Draft)**:
  > *"Many researchers have used machine learning for constitutive modeling. Ghaboussi et al. (1991) first used neural networks for material modeling. Later, Lefik and Schrefler (2003) applied ANNs to cyclic plasticity. Recently, Masi et al. (2021) proposed Thermodynamics-based Artificial Neural Networks (TANN) to satisfy thermodynamics. Also, Vlassis and Sun (2021) used Sobolev training for hyperelasticity and plasticity."*
- **After (Prof. WaiChing Sun Style — Concise Two-Sentence Cadence)**:
  > *"Early neural network constitutive models mapped strain histories directly to stress tensors using experimental data \cite{ghaboussi1991knowledge, lefik2003artificial}. Because these black-box architectures lack thermodynamic constraints, they can violate frame indifference or generate spurious energy along unseen loading paths. Recent thermodynamics-informed frameworks overcome this flaw by deriving stress and dissipation directly from learned free-energy and dissipation potentials \cite{masi2021thermodynamics, vlassis2021sobolev}. Supervising these potentials in Sobolev spaces further guarantees accurate algorithmic tangents for implicit finite element solvers."*

---

### Failure Mode 3: Blurring Governing PDEs vs. Constitutive Closures
- **Student Draft Symptom**: Calling the momentum balance or Darcy's law a "PDE model" without distinguishing universal conservation laws from material-dependent constitutive closures.
- **Fix**: Explicitly separate **universal balance principles** (mass, linear/angular momentum, first/second laws of thermodynamics, which hold regardless of material constitution) from **constitutive relations** (where material symmetry, history dependence, and data-driven surrogates enter).

---

### Failure Mode 4: Unmotivated Ad Hoc Assumptions
- **Student Draft Symptom**: Writing *"For simplicity, we assume temperature is constant and grains are incompressible"* without stating the physical regime or nondimensional number that justifies the assumption.
- **Fix**: Frame assumptions in terms of physical regimes: *"Restricting our attention to isothermal, quasi-static loading regimes where inertial effects and thermal expansion are negligible compared to hydro-mechanical skeleton deformation, the balance of linear momentum reduces to..."*

---

### Failure Mode 5: Loose Mathematical & Tensor Terminology
- **Student Draft Symptom**: Calling a second-order tensor a "matrix" when referring to an objective physical quantity, confusing coordinates with invariant tensors, or leaving norms/spaces unspecified (`"the error is small"` vs. `"the relative $L_2$ error falls below $10^{-3}$"`).
- **Fix**: Reserve "matrix" for Voigt/Kelvin algebraic representations or discretized finite element arrays (`\boldsymbol{K}`, `\boldsymbol{R}`); use "second-order tensor" (`\boldsymbol{\sigma}`, `\boldsymbol{\varepsilon}`) for continuum fields. Always specify the norm (`L_2`, `H^1`, `L_\infty`, Frobenius) when discussing errors or convergence.

---

### Failure Mode 6: Dangling Equations & Missing Symbol Definitions
- **Student Draft Symptom**: Dropping an equation block between two paragraphs with no punctuation and leaving half the subscripts undefined because "they are standard."
- **Fix**: Punctuate every equation block as part of the surrounding sentence and define every new symbol, operator, and domain immediately in the following `where`-clause.
