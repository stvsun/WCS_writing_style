---
name: waiching-sun-writing
description: >-
  Write, structure, and revise academic journal manuscripts, research grant
  proposals (DoD ARO/AFOSR/ONR, NSF, DOE), and student/co-author drafts in the
  authentic writing style, mathematical notation, and rhetorical structure of
  Prof. WaiChing Sun. Activate whenever drafting, editing, outlining, or
  polishing papers, proposals, white papers, abstracts, review responses, or
  LaTeX manuscripts in computational mechanics, poromechanics, or scientific
  machine learning.
---

# Prof. WaiChing Sun Academic Writing & Revision Skill (`waiching-sun-writing`)

## Overview

This skill equips the agent to write, structure, and revise journal articles, grant proposals, and student/co-author drafts in the authentic scholarly voice of **Prof. WaiChing Sun** (Columbia University), synthesized with the readability and audience principles of **Strunk & White's *The Elements of Style*** and **Booth, Colomb & Williams's *The Craft of Research* (Ch. 2, Ch. 11.5, Ch. 16.5, Ch. 17)**. It enforces:
- **Mechanistic & Mathematical Rigor**: Anchoring claims in conservation laws, thermodynamic admissibility (Coleman–Noll procedure, non-negative dissipation), frame indifference / material symmetry ($SO(3)$, Lie groups/algebras), and functional/Sobolev spaces.
- **Concision & Two-Sentence Splitting (*Elements of Style* + *Craft of Research* Ch. 17)**: Target a mean sentence length of **15–22 words** with a **hard ceiling of 28–30 words**. Whenever a sentence combines two technical moves (e.g., *mechanism + physical consequence*, or *limitation + remedy*), **break it into two crisp sentences** linked via **Old Before New** (Ch. 17.3), keeping grammatical subjects short and concrete (first 6–7 words, Ch. 17.2.2) and expressing actions in transitive verbs rather than stacked nominalizations (Ch. 17.2.3).
- **Audience & Concept-Difficulty Calibration (*Craft of Research* Ch. 2, Ch. 11.5, Ch. 16.5)**: Adapt explanation depth to how difficult or unfamiliar the concept is for the target reader:
  - **Tier 1 (Familiar / Standard Concepts for Specialist Peers)**: State in **1 compact sentence (12–18 words)**; omit textbook warrants.
  - **Tier 2 (High-Difficulty / Cross-Disciplinary Concepts, e.g., Lie algebras, Sobolev $H^1$ training, operator splitting)**: Unpack across **2–3 short sentences** using *Concrete Problem $\to$ Formal Mechanism $\to$ Explicit Warrant / Physical Intuition*.
  - **Tier 3 (Broad Scientific Audience / DoD & NSF Program Managers)**: Lead with the concrete engineering failure mode or capability gap in plain physical terms before introducing mathematical formalism, and close with the explicit *"So what?"* impact.
- **Grammatical Equation Integration**: Every equation is punctuated as part of a complete English sentence and followed immediately by symbol definitions using the group's standard tensor notation.

---

## Progressive Disclosure Reference Map

Before writing or editing any text, read **only** the reference files needed for the current task:

1. **Always Read First**:
   - [references/voice_and_rhetoric.md](./references/voice_and_rhetoric.md) — Core persona, **15–22 word sentence cadence & Two-Sentence Split Rule**, **3-Tier Audience & Concept-Difficulty Calibration Matrix**, *Craft of Research* Ch. 17 principles (*Short Concrete Subjects*, *Verbs over Nominalizations*, *Old Before New*, *Complexity Last*), and the strict **Anti-AI-Slop Blacklist**.
2. **When Writing Equations, Formulations, or LaTeX**:
   - [references/math_and_mechanics_notation.md](./references/math_and_mechanics_notation.md) — Continuum/poromechanics/SciML symbol conventions, standard notation paragraph, prose-equation punctuation rules, and `Remark`/`Proposition`/`Algorithm` usage.
   - [resources/wsun_macros.sty](./resources/wsun_macros.sty) — Standard LaTeX macro package (`\ten`, `\bsigma`, `\bsigmap`, `\beps`, `\Ctan`, etc.).
3. **When Drafting or Structuring a Journal Manuscript** (*CMAME*, *JMPS*, *IJNME*, *JCP*, *IJNAMG*, *Acta Geotechnica*, *WRR*, *Computers and Geotechnics*):
   - [references/journal_blueprints.md](./references/journal_blueprints.md) — Section-by-section blueprints (`Abstract` 4-move structure, `Introduction` 5-stage funnel, `Formulation`, `Numerical Examples` verification-to-validation progression, `Conclusion`).
   - [resources/journal_skeleton.tex](./resources/journal_skeleton.tex) — Full LaTeX manuscript template.
4. **When Drafting or Structuring a Grant Proposal or White Paper** (*DoD ARO/AFOSR/ONR*, *NSF CMMI/OAC/CAREER*, *DOE ASCR/BES*):
   - [references/proposal_blueprints.md](./references/proposal_blueprints.md) — Heilmeier Catechism framing, Hypothesis-driven Research Thrust architecture, NSF Project Summary & 15-page Project Description blueprints.
   - [resources/proposal_skeleton_dod.tex](./resources/proposal_skeleton_dod.tex) and [resources/proposal_skeleton_nsf.tex](./resources/proposal_skeleton_nsf.tex).
5. **When Revising or Rewriting a Student or Co-Author Draft**:
   - [references/student_revision_playbook.md](./references/student_revision_playbook.md) — 4-step revision protocol and solutions for the 6 common student draft failure modes (plot narration, annotated-bibliography literature reviews, loose tensor terminology, unmotivated assumptions, etc.).

---

## Operational Workflows

### Workflow 1: Journal Article Drafting & Section Writing
1. Read [references/voice_and_rhetoric.md](./references/voice_and_rhetoric.md), [references/math_and_mechanics_notation.md](./references/math_and_mechanics_notation.md), and [references/journal_blueprints.md](./references/journal_blueprints.md).
2. Identify the target journal family (Computational Mechanics vs. Geomechanics/Poromechanics) and the target section(s).
3. If starting a new LaTeX manuscript, copy [resources/wsun_macros.sty](./resources/wsun_macros.sty) and [resources/journal_skeleton.tex](./resources/journal_skeleton.tex).
4. Draft the prose and mathematical equations adhering strictly to the 3-part deductive paragraph structure and equation punctuation rules.
5. Run the **Mandatory Style Linter Verification** (below) before presenting the output.

### Workflow 2: Grant Proposal & White Paper Writing
1. Read [references/voice_and_rhetoric.md](./references/voice_and_rhetoric.md) and [references/proposal_blueprints.md](./references/proposal_blueprints.md).
2. Identify the funding agency (**DoD ARO/AFOSR/ONR**, **NSF CMMI/OAC/CAREER**, or **DOE ASCR/BES**) and document type (White Paper, Project Summary, or Full Technical Volume).
3. Anchor every Research Thrust around an explicit, falsifiable **Scientific Hypothesis**, the **Mathematical/Computational Mechanism**, the **Bidirectional Coupling** with other Thrusts, and a **Verification/Validation Metric**.
4. Run the **Mandatory Style Linter Verification** before presenting the output.

### Workflow 3: Co-Author / Student Draft Revision Mode
1. Read [references/student_revision_playbook.md](./references/student_revision_playbook.md) and [references/voice_and_rhetoric.md](./references/voice_and_rhetoric.md).
2. **Step 1 (Diagnose)**: Audit the input draft using `scripts/style_linter.py` and check for the 6 Student Draft Failure Modes (e.g., curve narration like *"the blue curve goes up"*, laundry-list literature reviews, unpunctuated equations).
3. **Step 2 (Restructure & Sharpen)**: Reorganize paragraphs so each opens with a physical/mathematical premise, integrate equations grammatically, and replace vague descriptions with mechanistic explanations.
4. **Step 3 (Verify)**: Run `scripts/style_linter.py` on the revised draft to confirm a score $\ge 90/100$ and zero errors.
5. **Step 4 (Report)**: Output the revised text alongside a concise bulleted **Revision Summary** explaining the key structural and technical upgrades made.

### Workflow 4: Updating the Skill from Local or Google Drive Corpus Files
Whenever Prof. Sun provides new local directory paths or Google Drive folders containing his papers, proposals, or before/after student drafts (strictly using only user-designated paths—never scraping public web repositories without instruction):

1. **Ingest & Classify Corpus**:
   ```bash
   python3 scripts/corpus_analyzer.py ingest \
     --paths "<user_designated_path_1>" "<user_designated_path_2>" \
     --output /tmp/wsun_corpus_manifest.json
   ```
2. **Extract LaTeX Macros & Environments**:
   ```bash
   python3 scripts/corpus_analyzer.py extract-latex \
     --manifest /tmp/wsun_corpus_manifest.json \
     --output /tmp/wsun_latex_profile.json
   ```
3. **Analyze Section & Category Stylometrics**:
   ```bash
   python3 scripts/corpus_analyzer.py analyze-style \
     --manifest /tmp/wsun_corpus_manifest.json \
     --output /tmp/wsun_style_profile.json
   ```
4. **Compare Student Before/After Draft Pairs** *(if provided)*:
   ```bash
   python3 scripts/corpus_analyzer.py compare-drafts \
     --before "<student_draft.tex>" \
     --after "<final_revised.tex>" \
     --output /tmp/wsun_diff_report.json
   ```
5. Incorporate newly discovered high-frequency macros into [resources/wsun_macros.sty](./resources/wsun_macros.sty) and newly extracted phrase patterns into `references/*.md`.

---

## Mandatory Style Linter Verification

Before returning any drafted or revised `.tex` or `.md` text to the user, run [scripts/style_linter.py](./scripts/style_linter.py) (resolve `scripts/style_linter.py` relative to this `SKILL.md` folder—e.g., `~/.claude/skills/waiching-sun-writing/scripts/style_linter.py`, `~/.codex/skills/waiching-sun-writing/scripts/style_linter.py`, or `~/.gemini/config/plugins/waiching-sun-writing/skills/waiching-sun-writing/scripts/style_linter.py`):

```bash
python3 "<path_to_this_skill_dir>/scripts/style_linter.py" check \
  --input <path_to_draft_file> \
  --output /tmp/wsun_lint_report.json
```

- Inspect `/tmp/wsun_lint_report.json`.
- If `error_count > 0` or `score < 85`, fix every flagged AI cliché, unpunctuated display equation, bare symbol sentence starter, or cadence warning and re-run the linter until `passed: true`.

---

## Common Mistakes to Avoid

1. **Writing Generic AI Transitions**: Never use *"delve into"*, *"tapestry"*, *"testament to"*, *"plays a crucial role"*, *"in the realm of"*, *"paves the way"*, or *"seamlessly"*.
2. **Narrating Plots Visually Instead of Mechanistically**: Never write *"In Fig. 3, the red curve is closer to the benchmark."* Explain **why** the mathematical formulation (e.g., polyconvexity, Sobolev $H^1$ regularization, operator splitting, Lie-group invariance) produces that physical or numerical behavior.
3. **Leaving Display Equations Unpunctuated**: Every `\begin{equation}` or `\begin{align}` block must end with `,` or `.` and have all newly introduced symbols defined immediately in the following `where`-clause.
