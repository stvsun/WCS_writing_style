#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Style Linter CLI for the `waiching-sun-writing` Antigravity Skill.

Audits LaTeX (.tex) or Markdown (.md) drafts against Prof. WaiChing Sun's
academic writing style, mathematical prose conventions, and anti-AI-slop rules.

Usage:
    python3 scripts/style_linter.py check --input draft.tex --output lint_report.json
"""

import argparse
import json
from pathlib import Path
import re
import statistics
import sys
from typing import Any, Dict, List, Tuple


AI_CLICHE_PATTERNS: List[Tuple[str, str, str]] = [
    (
        r"\bdelv(?:e|es|ed|ing)\b",
        "ai_cliche",
        "Avoid 'delve into'. State the mathematical or physical analysis directly (e.g., 'examine', 'formulate', 'investigate', 'analyze').",
    ),
    (
        r"\btapestry\b",
        "ai_cliche",
        "Never use 'tapestry'. Use precise mechanics/multiscale terminology (e.g., 'hierarchy', 'coupled system', 'microstructural manifold').",
    ),
    (
        r"\btestament to\b",
        "ai_cliche",
        "Avoid 'testament to'. State the quantitative verification or physical evidence directly.",
    ),
    (
        r"\bin the realm of\b",
        "ai_cliche",
        "Replace 'in the realm of' with the direct discipline or regime (e.g., 'in computational poromechanics', 'in the finite-strain regime').",
    ),
    (
        r"\bpaves? the way\b",
        "ai_cliche",
        "Replace 'paves the way' with a concrete technical consequence (e.g., 'enables', 'permits', 'provides a rigorous foundation for').",
    ),
    (
        r"\b(?:crucial|pivotal|vital|paramount)\s+role\b",
        "ai_cliche",
        "Avoid generic intensifiers like 'plays a crucial/pivotal role'. Specify *how* the mechanism governs the response (e.g., 'governs the onset of strain localization', 'controls the dissipation rate').",
    ),
    (
        r"\bunderscores?\s+the\s+(?:importance|need|significance)\b",
        "ai_cliche",
        "Avoid 'underscores the importance of'. State the mathematical requirement or physical consequence directly.",
    ),
    (
        r"\bseamless(?:ly)?\b",
        "ai_cliche",
        "Avoid 'seamless/seamlessly'. Describe the exact coupling or transition mechanism (e.g., 'monolithically coupled', 'consistently enforced via operator splitting').",
    ),
    (
        r"\bholistic(?:ally)?\b",
        "ai_cliche",
        "Avoid 'holistic'. Use 'unified', 'thermodynamically consistent', 'fully coupled', or 'end-to-end'.",
    ),
    (
        r"\b(?:groundbreaking|game-changing|revolutionary)\b",
        "ai_cliche",
        "Avoid promotional hype words. Establish novelty through precise contrast with prior formulations and mathematical guarantees.",
    ),
    (
        r"\bshed(?:s|ding)?\s+light\s+on\b",
        "ai_cliche",
        "Replace 'shed light on' with 'elucidate', 'characterize', 'quantify', or 'reveal the mechanism governing'.",
    ),
    (
        r"\bit is worth noting that\b",
        "verbose_filler",
        "Prefer concise 'Note that' or 'Notice that', or state the observation directly.",
    ),
    (
        r"\bin order to\b",
        "verbose_filler",
        "Tighten 'in order to' to 'to' (Strunk & White: Omit needless words).",
    ),
    (
        r"\b(?:due to the fact that|owing to the fact that|in light of the fact that)\b",
        "verbose_filler",
        "Replace verbose phrase with 'because' or 'since' (Elements of Style: Omit needless words).",
    ),
    (
        r"\b(?:utilize|utilizes|utilized|utilizing|utilization)\b",
        "verbose_filler",
        "Prefer 'use' over 'utilize/utilization' unless a specific resource-utilization metric is meant.",
    ),
    (
        r"(?:^|\.\s+)The\s+\w+(?:tion|ment|ance|ence)\s+of\b",
        "nominalization_subject",
        "Avoid opening a sentence with an abstract nominalization ('The [noun-tion] of...'). Make a concrete physical/mathematical entity the subject and express the action in the verb (Craft of Research Ch. 17.2).",
    ),
]

STUDENT_DRAFT_PATTERNS: List[Tuple[str, str, str]] = [
    (
        r"\b(?:the\s+(?:blue|red|green|black|orange|dashed|solid|dotted)\s+(?:line|curve)\s+(?:goes\s+up|goes\s+down|is\s+higher|is\s+lower))\b",
        "student_narration",
        "Avoid superficial curve narration ('the blue line goes up'). Explain the physical mechanism, constitutive response, or convergence rate illustrated by the curve.",
    ),
    (
        r"\b(?:as\s+we\s+can\s+see\s+in\s+(?:fig|figure)|looking\s+at\s+(?:fig|figure))\b",
        "student_narration",
        "Avoid conversational plot pointers ('as we can see in Fig.'). Lead with the physical observation and cite the figure parenthetically or via 'As shown in Fig. X,'.",
    ),
    (
        r"(?:^|\.\s+)Equation\s+\(\d+\)\s+(?:shows|gives|is)\b",
        "equation_prose",
        "Prefer leading with the physical/mathematical quantity rather than starting a sentence with 'Equation (X) shows...'.",
    ),
    (
        r"\$(?:\\bf|\\textbf)\b",
        "latex_notation",
        "Do not use \\bf or \\textbf inside math mode for tensors/vectors; use \\boldsymbol{...}, \\bm{...}, or the standard macros in wsun_macros.sty.",
    ),
]


def check_display_equation_punctuation(tex: str) -> List[Dict[str, Any]]:
    """Verify that display equations end with proper sentence punctuation (, . ;)."""
    issues: List[Dict[str, Any]] = []
    env_pattern = re.compile(
        r"\\begin\{(equation|align|gather|multline)\}(.*?)\\end\{\1\}",
        re.DOTALL,
    )
    for match in env_pattern.finditer(tex):
        env_name = match.group(1)
        body = match.group(2)
        start_line = tex[: match.start()].count("\n") + 1
        # Strip comments and trailing labels/whitespace
        cleaned = re.sub(r"(?<!\\)%.*$", "", body, flags=re.MULTILINE)
        cleaned = re.sub(r"\\label\{[^}]*\}", "", cleaned)
        cleaned = re.sub(r"\\nonumber|\\notag", "", cleaned)
        cleaned = cleaned.strip()
        if cleaned and cleaned[-1] not in {",", ".", ";"}:
            issues.append(
                {
                    "line": start_line,
                    "severity": "warning",
                    "category": "equation_punctuation",
                    "message": f"Display environment '\\begin{{{env_name}}}' does not end with sentence punctuation (',' or '.').",
                    "suggestion": "In Prof. Sun's style, every display equation is part of a grammatical sentence and must end with ',' or '.' before \\end{...}.",
                }
            )
    return issues


def check_sentence_starts_with_symbol(tex: str) -> List[Dict[str, Any]]:
    """Flag sentences that begin directly with inline math '$...$'."""
    issues: List[Dict[str, Any]] = []
    for idx, line in enumerate(tex.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("%"):
            continue
        if re.search(r"(?:^|\.\s+)\$[^$]+\$\s+(?:is|are|denotes|represents)\b", stripped):
            issues.append(
                {
                    "line": idx,
                    "severity": "warning",
                    "category": "math_prose_hygiene",
                    "message": "Sentence begins directly with a bare mathematical symbol ($...$).",
                    "suggestion": "Precede the symbol with its physical or mathematical descriptor (e.g., 'The Cauchy stress tensor $\\boldsymbol{\\sigma}$ denotes...').",
                }
            )
    return issues


def lint_text(text: str, is_tex: bool = True) -> Dict[str, Any]:
    """Run all style, notation, and cadence checks on input text."""
    if not is_tex and "Response to Reviewer" in text:
        paras = [p.strip() for p in text.split("\n\n") if p.strip()]
        author_paras = [
            p.strip("“”")
            for p in paras
            if p.startswith("Please find")
            or p.startswith("Thank you")
            or p.startswith("Response:")
            or p.startswith("“")
        ]
        if author_paras:
            text = "\n\n".join(author_paras)

    issues: List[Dict[str, Any]] = []
    lines = text.splitlines()

    for line_idx, raw_line in enumerate(lines, start=1):
        line = re.sub(r"(?<!\\)%.*$", "", raw_line) if is_tex else raw_line
        if not line.strip():
            continue

        for pat, cat, suggestion in AI_CLICHE_PATTERNS + STUDENT_DRAFT_PATTERNS:
            m = re.search(pat, line, flags=re.IGNORECASE)
            if m:
                issues.append(
                    {
                        "line": line_idx,
                        "severity": "error" if cat == "ai_cliche" else "warning",
                        "category": cat,
                        "matched": m.group(0),
                        "message": f"Flagged pattern '{m.group(0)}' ({cat}).",
                        "suggestion": suggestion,
                    }
                )

    # Check excessive em-dashes
    emdash_count = len(re.findall(r"---|—", text))
    word_count = max(len(text.split()), 1)
    if emdash_count * 1000.0 / word_count > 3.5:
        issues.append(
            {
                "line": 1,
                "severity": "warning",
                "category": "punctuation_cadence",
                "message": f"High em-dash frequency ({emdash_count} occurrences in {word_count} words).",
                "suggestion": "Prof. Sun rarely uses em-dashes in technical prose; prefer parentheses, colons, or structured subordinate clauses.",
            }
        )

    if is_tex:
        issues.extend(check_display_equation_punctuation(text))
        issues.extend(check_sentence_starts_with_symbol(text))

    # Compute sentence cadence summary
    clean = re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE) if is_tex else text
    if "\\begin{document}" in clean:
        clean = clean.split("\\begin{document}", 1)[1]
    if "\\end{document}" in clean:
        clean = clean.split("\\end{document}", 1)[0]
    clean = re.sub(r"\\maketitle", ". ", clean)
    clean = re.sub(
        r"\\(?:sub)*section\*?\{[^}]*\}|\\label\{[^}]*\}",
        ". ",
        clean,
    )
    clean = re.sub(
        r"\\begin\{(?:equation\*?|align\*?|gather\*?|algorithm|thebibliography)\}.*?\\end\{(?:equation\*?|align\*?|gather\*?|algorithm|thebibliography)\}",
        " [EQ] ",
        clean,
        flags=re.DOTALL,
    )
    clean = re.sub(r"\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?", ". ", clean)
    clean = re.sub(r"\$[^$]+\$", "[MATH]", clean)
    clean = re.sub(r"\\[a-zA-Z]+\*?\{([^}]*)\}", r"\1", clean)
    clean = re.sub(r"\\[a-zA-Z]+", " ", clean)

    raw_sents = re.split(r"(?<=[.!?])\s+(?=[A-Z\[])", re.sub(r"\s+", " ", clean))
    sents = [s.strip() for s in raw_sents if 4 <= len(s.strip().split()) <= 120]
    sent_lengths = [
        len(s.split())
        for s in sents
        if "[EQ]" not in s and "bold-faced letters denote tensors" not in s.lower()
    ]

    # Flag individual overly long sentences (> 30 words), excluding standard notation/where lists
    long_sentence_count = 0
    for s in sents:
        words = s.split()
        w_count = len(words)
        lower_s = s.lower()
        is_exempt = (
            lower_s.startswith("where ")
            or "[eq]" in lower_s
            or "bold-faced letters denote tensors" in lower_s
        )
        if w_count > 30 and not is_exempt:
            long_sentence_count += 1
            snippet = " ".join(words[:10]) + " ..."
            issues.append(
                {
                    "line": 1,
                    "severity": "warning",
                    "category": "long_sentence",
                    "matched": snippet,
                    "message": f"Sentence exceeds 30-word readability ceiling ({w_count} words): '{snippet}'",
                    "suggestion": "Break into two sentences following 'Old Before New' (Craft of Research Ch. 17.3): state the premise/mechanism in Sentence 1, and open Sentence 2 with a backward-linking subject ('This formulation...', 'Such regularization...').",
                }
            )
        # Check nominalization overload (>= 4 abstract nominalizations in one sentence)
        nom_matches = re.findall(
            r"\b[a-zA-Z]{5,}(?:tion|tions|ment|ments|ence|ences|ance|ances)\b", s
        )
        if len(nom_matches) >= 4 and not is_exempt:
            issues.append(
                {
                    "line": 1,
                    "severity": "warning",
                    "category": "nominalization_overload",
                    "matched": ", ".join(nom_matches[:5]),
                    "message": f"Sentence contains {len(nom_matches)} abstract nominalizations ({', '.join(nom_matches[:4])}).",
                    "suggestion": "Turn abstract nouns (-tion/-ment/-ence) into active transitive verbs (Craft of Research Ch. 17.2.3).",
                }
            )

    mean_len = round(statistics.mean(sent_lengths), 2) if sent_lengths else 0.0
    if sent_lengths and mean_len < 12.0:
        issues.append(
            {
                "line": 1,
                "severity": "warning",
                "category": "sentence_cadence",
                "message": f"Mean sentence length is unusually short ({mean_len} words; target range 15-22 words).",
                "suggestion": "Link choppy sentences using 'Old Before New' transitions ('Consequently,...', 'By contrast,...').",
            }
        )
    elif sent_lengths and mean_len > 24.0:
        issues.append(
            {
                "line": 1,
                "severity": "warning",
                "category": "sentence_cadence",
                "message": f"Mean sentence length is too long ({mean_len} words; target range 15-22 words, hard ceiling 28-30 words).",
                "suggestion": "Split compound-complex sentences into two crisp sentences and omit needless words (Elements of Style + Craft of Research Ch. 17).",
            }
        )

    error_count = sum(1 for i in issues if i["severity"] == "error")
    warning_count = sum(1 for i in issues if i["severity"] == "warning")
    score = max(0, 100 - error_count * 15 - warning_count * 5)

    return {
        "passed": error_count == 0 and score >= 80,
        "score": score,
        "error_count": error_count,
        "warning_count": warning_count,
        "metrics": {
            "sentence_count": len(sents),
            "mean_sentence_length_words": mean_len,
            "median_sentence_length_words": round(statistics.median(sent_lengths), 2)
            if sent_lengths
            else 0.0,
            "emdash_count": emdash_count,
        },
        "issues": issues,
    }


def cmd_check(args: argparse.Namespace) -> int:
    in_path = Path(args.input).expanduser().resolve()
    if not in_path.exists():
        sys.stderr.write(f"[ERROR] Input file not found: {in_path}\n")
        return 1

    raw = in_path.read_text(encoding="utf-8", errors="replace")
    is_tex = in_path.suffix.lower() in {".tex", ".sty"}
    report = lint_text(raw, is_tex=is_tex)
    report["input_file"] = str(in_path)

    out_path = Path(args.output).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    status = "PASSED" if report["passed"] else "NEEDS_REVISION"
    print(
        f"Style lint [{status}] (Score: {report['score']}/100, Errors: {report['error_count']}, Warnings: {report['warning_count']}). Report written to: {out_path}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Style Linter for Prof. WaiChing Sun's Writing Skill."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="Audit a draft file against style rules.")
    p_check.add_argument("--input", required=True, help="Path to draft .tex or .md file.")
    p_check.add_argument(
        "--output", required=True, help="Path to write JSON lint report."
    )
    p_check.set_defaults(func=cmd_check)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
