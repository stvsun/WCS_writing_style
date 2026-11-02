# Mathematical, Continuum Mechanics, and SciML Notation Conventions

## 1. Tensor, Continuum Mechanics, and Poromechanics Notation

Prof. WaiChing Sun's manuscripts follow strict notation conventions in continuum mechanics, poromechanics, and geometric mechanics. Whenever writing or editing equations, enforce these defaults (unless a specific manuscript's existing preamble defines otherwise):

### Preliminary Notation Paragraph (End of Introduction)
Include a standard **Notation and Conventions** paragraph at the end of Section 1 (`Introduction`) in rigorous mechanics papers:
> *"As for notations and symbols, bold-faced letters denote tensors (including vectors which are rank-one tensors); the symbol '$\cdot$' denotes a single contraction of adjacent indices of two tensors (e.g., $\boldsymbol{a} \cdot \boldsymbol{b} = a_i b_i$ or $\boldsymbol{A} \cdot \boldsymbol{b} = A_{ij} b_j$); the symbol '$:$' denotes a double contraction of adjacent indices of tensor of rank two or higher (e.g., $\boldsymbol{A} : \boldsymbol{B} = A_{ij} B_{ij}$ or $\mathbb{C} : \boldsymbol{\varepsilon} = C_{ijkl} \varepsilon_{kl}$); the symbol '$\otimes$' denotes a juxtaposed tensor product (e.g., $(\boldsymbol{a} \otimes \boldsymbol{b})_{ij} = a_i b_j$)."*

### Standard Symbol Table
| Physical / Mathematical Quantity | Preferred LaTeX Notation | Notes |
| :--- | :--- | :--- |
| Vectors & 2nd-order tensors | `\boldsymbol{\sigma}`, `\boldsymbol{\varepsilon}`, `\boldsymbol{u}`, `\boldsymbol{F}` | Never use `\bf` or `\vec{x}` with overhead arrows for continuum fields |
| 4th-order tensors | `\mathbb{C}`, `\mathbb{E}`, `\mathbb{I}` | Blackboard bold for 4th-order tangent/elasticity tensors |
| Function spaces & manifolds | `\mathcal{V}`, `\mathcal{Q}`, `\mathcal{M}`, `\mathcal{S}`, `H^1(\Omega)` | Calligraphic for trial/test spaces and smooth manifolds |
| Lie groups & Lie algebras | `GL^+(3)`, `SO(3)`, `\mathfrak{so}(3)`, `\mathfrak{gl}(3)` | `\mathfrak` for Lie algebras; `\exp` and `\log` maps |
| Reference vs. current configuration | `\mathcal{B}_0 \subset \mathbb{R}^3`, `\mathcal{B}_t` | Material coordinates `\boldsymbol{X}`, spatial `\boldsymbol{x} = \boldsymbol{\varphi}(\boldsymbol{X}, t)` |
| Deformation & strain measures | `\boldsymbol{F} = \nabla_{\boldsymbol{X}} \boldsymbol{\varphi}`, `\boldsymbol{C} = \boldsymbol{F}^{\mathrm{T}}\boldsymbol{F}`, `\boldsymbol{E}`, `\boldsymbol{\varepsilon} = \operatorname{sym}(\nabla \boldsymbol{u})` | Always use upright `\mathrm{T}` for transpose and `\operatorname{sym}` / `\operatorname{skw}` |
| Stress measures | `\boldsymbol{\sigma}` (Cauchy), `\boldsymbol{P}` (1st PK), `\boldsymbol{S}` (2nd PK), `\boldsymbol{\sigma}'` (effective stress) | Explicitly state effective stress sign convention (tension positive in mechanics vs. compression positive in geomechanics) |
| Poromechanics fields | `p` or `p_{\mathrm{f}}` (pore pressure), `\phi` or `n` (porosity), `\boldsymbol{k}` (intrinsic permeability), `B` (Skempton), `\alpha` (Biot coefficient) | Distinguish Darcy velocity `\boldsymbol{q}` from relative fluid velocity |
| Thermodynamic potentials | `\psi` or `\Psi` (Helmholtz free energy), `\mathcal{D} \ge 0` (internal dissipation), `\boldsymbol{\alpha}` (internal state variables) | Always pair constitutive laws with the Coleman–Noll procedure / dissipation inequality |
| Neural / SciML parameters | `\boldsymbol{\theta} \in \mathbb{R}^{N_{\theta}}`, `\mathcal{NN}_{\boldsymbol{\theta}}`, `\mathcal{L}(\boldsymbol{\theta})` | Sobolev norms `\|\cdot\|_{W^{k,p}}` or `\|\cdot\|_{H^1}` when training with derivative supervision |

---

## 2. Grammatical Integration of Equations into Prose

1. **Equations Are Part of Sentences**:
   Every display equation (`equation`, `align`, `gather`) is a syntactic clause inside a complete English sentence and **must end with a comma `,` or period `.`** before `\end{equation}` or `\end{align}`.
2. **Never Start a Sentence with a Bare Symbol or Number**:
   - *Incorrect*: `$\boldsymbol{\sigma}'$ is the Biot effective stress tensor. Equation (4) shows the mass balance.`
   - *Correct*: `Here, $\boldsymbol{\sigma}'$ denotes the Biot effective stress tensor. Furthermore, the mixture mass balance in Eq. (4) couples the solid skeleton volumetric strain rate with fluid storage.`
3. **Immediate Symbol Definition Clause**:
   Immediately after introducing a governing equation, define all newly introduced symbols in a structured `where`-clause:
   ```latex
   \begin{equation}
     \nabla \cdot \left( \boldsymbol{\sigma}' - b p \boldsymbol{I} \right) + \rho \boldsymbol{g} = \boldsymbol{0} \quad \text{in } \Omega,
     \label{eq:linear_momentum}
   \end{equation}
   where $\boldsymbol{\sigma}'$ denotes the effective Cauchy stress tensor, $b \in [0, 1]$ is the Biot coefficient, $p$ is the pore fluid pressure, $\boldsymbol{I}$ is the second-order identity tensor, $\rho = (1 - \phi)\rho_{\mathrm{s}} + \phi \rho_{\mathrm{f}}$ is the homogenized mixture density, and $\boldsymbol{g}$ is the gravitational acceleration vector.
   ```

---

## 3. Strategic Use of `Remark`, `Proposition`, `Definition`, and `Algorithm`

A hallmark of Prof. Sun's journal papers is the disciplined use of numbered `Remark` and `Proposition` environments to separate core derivation flow from critical theoretical insights:

1. **When to Use a `\begin{remark} ... \end{remark}` Block**:
   - To explain **limiting cases** (e.g., how the general multiphase or nonlocal formulation recovers classical Terzaghi/Biot poroelasticity or local $J_2$ plasticity as a length scale $\ell \to 0$ or permeability $\|\boldsymbol{k}\| \to \infty$).
   - To highlight **computational or implementation subtleties** (e.g., why Sobolev $H^1$ training is required so the neural network's consistent tangent $\partial^2 \psi_{\boldsymbol{\theta}} / \partial \boldsymbol{\varepsilon}^2$ remains accurate inside a Newton–Raphson solver).
   - To clarify **frame indifference vs. material symmetry** distinctions that readers or reviewers might conflate.
2. **When to Use a `\begin{proposition}` / `\begin{definition}` Block**:
   - When establishing thermodynamic admissibility, convexity/polyconvexity guarantees, Nash equilibrium existence in meta-modeling games, or stability bounds.
3. **How to Present `\begin{algorithm}` Blocks**:
   - Every algorithm block must have explicit `\textbf{Input:}` (or `\Require`) and `\textbf{Output:}` (or `\Ensure`) headers, numbered steps corresponding to equations in the text (e.g., *"Compute trial elastic predictor via Eq. \eqref{eq:trial}"*), and a concise prose walkthrough in the main text explaining the computational complexity and data flow.
