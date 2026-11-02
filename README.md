# `WCS_writing_style` (`waiching-sun-writing`) — Multi-Agent Academic Writing Skill for Prof. WaiChing Sun

This repository houses the **`waiching-sun-writing`** skill for **Google Antigravity**, **Claude Code**, and **OpenAI Codex**. It is designed to draft, structure, and revise academic journal manuscripts, research grant proposals (DoD ARO/AFOSR/ONR, NSF CMMI/OAC/CAREER, DOE ASCR/BES), and student/co-author drafts in the authentic writing style, mathematical notation, and rhetorical structure of **Prof. WaiChing Sun** (Columbia University), synthesized with *The Elements of Style* and *The Craft of Research*.

---

## Global Installation Across All Computers (Antigravity + Claude Code + Codex)

Running `./install.sh` installs `waiching-sun-writing` globally for **all three AI coding agents** on any Mac or Linux machine:
1. **Google Antigravity**: `~/.gemini/config/plugins/waiching-sun-writing`
2. **Claude Code**: `~/.claude/skills/waiching-sun-writing`
3. **OpenAI Codex**: `~/.codex/skills/waiching-sun-writing` (including `agents/openai.yaml` for `$waiching-sun-writing`)

### Option A: Via Private GitHub Repository (`WCS_writing_style` — Recommended)
On any computer where you are signed into GitHub, clone the private repository and run `./install.sh`:

```bash
git clone https://github.com/stvsun/WCS_writing_style.git
cd WCS_writing_style
./install.sh
```

*(If using `gh` CLI: `gh repo clone stvsun/WCS_writing_style && cd WCS_writing_style && ./install.sh`)*

To pull future updates on any computer:
```bash
cd WCS_writing_style
git pull
./install.sh
```

### Option B: Via Google Drive / Shared Cloud Folder
Copy or sync the `WCS_writing_style` folder via Google Drive or Dropbox, open a terminal inside the folder on that machine, and run:
```bash
./install.sh
```

---

## How to Call the Skill in Each Agent

- **In Google Antigravity**:
  - Automatically activates on paper/proposal writing tasks, or mention `waiching-sun-writing` in your prompt.
- **In Claude Code (`claude`)**:
  - Automatically discovered from `~/.claude/skills/waiching-sun-writing/SKILL.md`, or prompt: *"Use `waiching-sun-writing` to revise..."*
- **In OpenAI Codex (`codex`)**:
  - Automatically discovered from `~/.codex/skills/waiching-sun-writing/SKILL.md`, or invoke directly via `$waiching-sun-writing`.

---

## Repository Structure

```text
.
├── install.sh                                # One-step installer for Antigravity, Claude Code & Codex
├── plugin.json                               # Antigravity global plugin manifest
├── CLAUDE.md                                 # Project instructions for Claude Code
├── AGENTS.md                                 # Project instructions for OpenAI Codex & Antigravity
├── assets/
│   └── logo.svg                              # Plugin icon
└── skills/waiching-sun-writing/
    ├── SKILL.md                              # Main skill entrypoint & workflow router
    ├── agents/
    │   └── openai.yaml                       # OpenAI Codex UI metadata ($waiching-sun-writing)
    ├── scripts/
    │   ├── corpus_analyzer.py                # CLI to extract style metrics & LaTeX macros from local/GDrive folders
    │   └── style_linter.py                   # Deterministic CLI linter to audit drafts against Prof. Sun's style
    ├── references/
    │   ├── voice_and_rhetoric.md             # Concise 15-22 word cadence, Two-Sentence Split Rule & 3-Tier Audience Matrix
    │   ├── math_and_mechanics_notation.md    # Tensor/continuum/poromechanics notation, equation grammar, Remark blocks
    │   ├── journal_blueprints.md             # Section blueprints for CMAME, JMPS, IJNME, JCP, IJNAMG, Acta Geotech, WRR
    │   ├── proposal_blueprints.md            # Agency blueprints for DoD (ARO/AFOSR/ONR), NSF, and DOE proposals
    │   └── student_revision_playbook.md      # 4-step protocol & Before/After fixes for student draft failure modes
    └── resources/
        ├── wsun_macros.sty                   # Consolidated LaTeX macros (\ten, \bsigma, \bsigmap, \beps, \Ctan, etc.)
        ├── journal_skeleton.tex              # Ready-to-compile LaTeX manuscript template
        ├── proposal_skeleton_dod.tex         # DoD Basic Research White Paper / Proposal template
        └── proposal_skeleton_nsf.tex         # NSF Project Summary & 15-Page Project Description template
```

---

## Auditing Drafts with the Style Linter

```bash
python3 skills/waiching-sun-writing/scripts/style_linter.py check \
  --input path/to/draft.tex \
  --output /tmp/lint_report.json
```
