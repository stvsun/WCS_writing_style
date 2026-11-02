# Voice, Cadence, and Rhetorical Signature (Prof. WaiChing Sun)

Grounded in **Strunk & White's *The Elements of Style*** and **Booth, Colomb, Williams, Bizup & FitzGerald's *The Craft of Research* (4th Ed., especially Ch. 2, 11, 16, and 17)**, this guide codifies Prof. WaiChing Sun's prose style: **mathematically rigorous, concise, and immediately readable by humans**.

---

## 1. Core Authorial Persona

1. **Mechanistic & Mathematical Precision Without Bloated Syntax**:
   Anchor claims in physical laws (mass/momentum balance, second-law dissipation, frame indifference) and mathematical structure (Sobolev spaces, Lie groups, operator splits), but **never** pack three mechanisms into a single breathless sentence.
2. **Omit Needless Words (*Elements of Style*, Rule 17)**:
   Every word must tell. Strip throat-clearing openings, redundant modifiers, and stacked prepositional chains (*"the characterization of the evolution of..."*).
3. **Break Long Sentences Into Two**:
   When a sentence contains both a complex premise and a technical mechanism or consequence, **split it into two sentences**.

---

## 2. Four Principles of Clear, Concise Sentences (*The Craft of Research*, Ch. 17)

### Target Sentence Length
- **Target Mean Sentence Length**: **15–22 words**.
- **Hard Ceiling**: **28 words per sentence**. Any sentence exceeding 28–30 words **must** be broken into two sentences.

### Principle 1: Short, Concrete Subjects in the First 6–7 Words (Ch. 17.2.2)
Readers judge a sentence's clarity by its first six or seven words. Make the grammatical subject short, specific, and concrete (`Nested FE² schemes...`, `These surrogates...`, `We...`, `The Biot effective stress...`) so the reader reaches the main verb immediately.
- *Bad (Long abstract subject)*: *"Predictive simulation of fluid-infiltrated porous media undergoing inelastic deformation across multiple spatial scales without incurring high cost requires..."* (18 words before the verb!)
- *Good (Short subject + strong verb)*: *"Simulating fluid-infiltrated porous media requires constitutive closures that link pore-scale kinematics to macroscopic balance laws."*

### Principle 2: Express Crucial Actions in Verbs, Not Nominalizations (Ch. 17.2.3)
Do not turn action verbs into abstract nouns ending in *-tion, -ment, -ence, -ity* paired with weak verbs (`make`, `provide`, `achieve`, `perform`, `occur`). Keep technical nouns only when they name standard mathematical objects (`stress`, `dissipation`, `homogenization`).
- *Bad (Nominalized)*: *"The enforcement of polyconvexity provides the preservation of ellipticity during the occurrence of softening."*
- *Good (Verb-driven)*: *"Enforcing polyconvexity preserves ellipticity during post-peak softening."*

### Principle 3: Old Before New — The Two-Sentence Split Rule (Ch. 17.3)
When breaking a long sentence into two, link them using **Old Before New**:
1. **Sentence 1** states the core claim and ends with the new concept.
2. **Sentence 2** begins (in its first 6–7 words) with a short reference to that concept (*"This formulation..."*, *"These unconstrained mappings..."*, *"Under such loading..."*) and develops its consequence.

### Principle 4: Complexity Last (Ch. 17.5)
Place newly introduced technical terms, mathematical spaces, or long qualifying clauses at the **end** of a sentence, never at the beginning.

---

## 3. Calibrating Explanation Depth by Audience & Concept Difficulty (*Craft of Research*, Ch. 2, 11.5, 16.5)

As established in *The Craft of Research* (Ch. 11.5 *Knowing When to State a Warrant* and Ch. 16.5 *Setting the Right Pace*), experts find over-explaining basic concepts condescending, whereas readers encountering a novel cross-disciplinary concept get lost if the connecting logic (*warrant*) is omitted. Always calibrate detail across three tiers:

| Tier | Concept Difficulty & Target Audience | Pacing & Explanation Rule |
| :--- | :--- | :--- |
| **Tier 1: Familiar Concepts for Domain Peers** | Standard mechanics/math concepts for specialist reviewers (e.g., Cauchy stress, momentum balance, Newton–Raphson in *CMAME* / *JMPS*). | **Brisk & Compact (1 sentence, omit basic warrants).** State the assumption and equation directly without textbook definitions. |
| **Tier 2: High-Difficulty / Cross-Disciplinary Concepts** | Concepts crossing fields (e.g., explaining Lie algebras/Riemannian manifolds or game theory to mechanicians, or Coleman–Noll thermodynamics to ML readers). | **Two-Step Scaffolding (State the warrant explicitly).** *Sentence 1*: State the physical/computational problem in plain terms. *Sentence 2*: Introduce the mathematical tool at the end and state *why* it resolves that problem. |
| **Tier 3: Broad Scientific Audience / Program Managers** | Proposals, White Papers (ARO/AFOSR/ONR, NSF Summary), or general-audience abstracts. | **Concrete Cost & "So What?" First (Ch. 4.2 & 16.3).** *Sentence 1*: State what fails in engineering/defense practice and its tangible cost. *Sentence 2*: State the core innovation and its practical payoff. |

---

## 4. Signature Transition Phrasebank (Concise Forms)

Prefer short, crisp sentence connectors over wordy clauses:
- **Contrast**: *"However,"*, *"In contrast,"*, *"Conversely,"*, *"Yet"*
- **Precision**: *"Specifically,"*, *"In particular,"*, *"Here,"*, *"Note that"*
- **Cause / Consequence**: *"Consequently,"*, *"As a result,"*, *"Therefore,"*, *"Thus,"*
- **Purpose (Omit 'in order to')**: *"To overcome this limitation, we..."*, *"To regularize the tangent operator, we..."*

---

## 5. Strict Anti-AI-Slop & Wordiness Blacklist

| Forbidden Phrase / Pattern | Why It Fails | Concise WaiChing Sun Replacement |
| :--- | :--- | :--- |
| *"delve into" / "tapestry" / "testament to"* | LLM clichés | *"examine"*, *"coupled system"*, *"demonstrates"* |
| *"plays a crucial / pivotal / vital role"* | Vague filler | Use an action verb: *"governs"*, *"controls"*, *"dictates"* |
| *"in the realm of"* | Wordy filler | *"in"* (e.g., *"in computational poromechanics"*) |
| *"paves the way for"* | Cliché | *"enables"*, *"permits"* |
| *"seamless / holistic / groundbreaking"* | Marketing hype | *"monolithic"*, *"unified"*, *"thermodynamically consistent"* |
| *"it is worth noting that" / "in order to"* | Strunk & White wordiness | *"Note that"* (or delete) / *"to"* |
| Sentences > 28–30 words | Hard for humans to parse | Split into two sentences using **Old Before New** |
