#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Corpus Analyzer CLI for the `waiching-sun-writing` Antigravity Skill.

Extracts empirical writing style signatures, section-level rhetorical patterns,
LaTeX macro definitions, theorem/remark environment usage, and before/after
revision diffs from local or Google Drive directories designated by
Prof. WaiChing Sun.

Usage:
    python3 scripts/corpus_analyzer.py ingest --paths <dir1> [<dir2> ...] --output manifest.json
    python3 scripts/corpus_analyzer.py extract-latex --manifest manifest.json --output latex_profile.json
    python3 scripts/corpus_analyzer.py analyze-style --manifest manifest.json --output style_profile.json
    python3 scripts/corpus_analyzer.py compare-drafts --before student.tex --after final.tex --output diff_report.json
"""

import argparse
from collections import Counter, defaultdict
import difflib
import json
import os
from pathlib import Path
import re
import statistics
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from typing import Any, Dict, List, Optional, Tuple


SUPPORTED_EXTENSIONS = {".tex", ".sty", ".bib", ".docx", ".pdf", ".md", ".txt"}

PROPOSAL_KEYWORDS = {
    "proposal",
    "whitepaper",
    "white_paper",
    "heilmeier",
    "aro",
    "afosr",
    "onr",
    "nsf",
    "doe",
    "career",
    "cmmi",
    "ascr",
    "bes",
    "broader_impacts",
    "intellectual_merit",
    "project_description",
    "project_summary",
    "thrust",
    "bAA",
    "foa",
}

JOURNAL_KEYWORDS = {
    "cmame",
    "jmps",
    "ijnme",
    "ijnamg",
    "jcp",
    "elsarticle",
    "manuscript",
    "paper",
    "acta_geotechnica",
    "wrr",
    "comp_geotech",
}

TRANSITION_PHRASES = [
    "However,",
    "In contrast,",
    "On the other hand,",
    "Specifically,",
    "In particular,",
    "Consequently,",
    "Therefore,",
    "Furthermore,",
    "Moreover,",
    "Meanwhile,",
    "Nevertheless,",
    "Nonetheless,",
    "To address this",
    "To overcome this",
    "To circumvent this",
    "To remedy this",
    "Notice that",
    "Note that",
    "It is worth noting that",
    "It should be noted that",
    "Here,",
    "Herein,",
    "In this work,",
    "In this study,",
    "In this paper,",
    "For instance,",
    "For example,",
    "As a result,",
    "By contrast,",
]

POST_EQUATION_STARTERS = [
    "where",
    "with",
    "in which",
    "Here,",
    "Note that",
    "Notice that",
    "Consequently,",
    "Thus,",
    "Hence,",
]


def extract_text_from_docx(path: Path) -> str:
    """Extract plain text paragraphs from a .docx file using stdlib zipfile + XML."""
    try:
        with zipfile.ZipFile(path, "r") as zf:
            if "word/document.xml" not in zf.namelist():
                return ""
            xml_content = zf.read("word/document.xml")
        tree = ET.fromstring(xml_content)
        namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        paragraphs = []
        for p in tree.findall(".//w:p", namespace):
            texts = [t.text for t in p.findall(".//w:t", namespace) if t.text]
            if texts:
                paragraphs.append("".join(texts))
        return "\n\n".join(paragraphs)
    except Exception as exc:
        sys.stderr.write(f"[WARN] Failed to read docx {path}: {exc}\n")
        return ""


def extract_text_from_pdf(path: Path) -> str:
    """Extract text from PDF if pdftotext is available on the system."""
    try:
        res = subprocess.run(
            ["pdftotext", str(path), "-"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout
    except FileNotFoundError:
        pass
    except Exception as exc:
        sys.stderr.write(f"[WARN] pdftotext failed on {path}: {exc}\n")
    return ""


def strip_latex_comments(tex: str) -> str:
    """Remove unescaped LaTeX comments while preserving line structure."""
    lines = []
    for line in tex.splitlines():
        cleaned = re.sub(r"(?<!\\)%.*$", "", line)
        lines.append(cleaned)
    return "\n".join(lines)


def classify_document(path: Path, raw_text: str) -> str:
    """Classify a document into journal_manuscript, grant_proposal, macro_package, etc."""
    ext = path.suffix.lower()
    if ext == ".sty":
        return "macro_package"
    if ext == ".bib":
        return "bibliography"

    path_lower = str(path).lower()
    sample_lower = raw_text[:8000].lower()

    if any(k in path_lower for k in ("student", "draft_v1", "before", "rough")):
        return "student_draft"

    proposal_hits = sum(
        1 for kw in PROPOSAL_KEYWORDS if kw.lower() in path_lower or kw.lower() in sample_lower
    )
    journal_hits = sum(
        1 for kw in JOURNAL_KEYWORDS if kw.lower() in path_lower or kw.lower() in sample_lower
    )

    if (
        "intellectual merit" in sample_lower
        or "broader impacts" in sample_lower
        or "research thrust" in sample_lower
        or "white paper" in sample_lower
        or proposal_hits > journal_hits + 1
    ):
        return "grant_proposal"
    return "journal_manuscript"


def cmd_ingest(args: argparse.Namespace) -> int:
    """Ingest and classify files from user-designated paths."""
    records: List[Dict[str, Any]] = []
    category_counts: Counter = Counter()

    for raw_p in args.paths:
        target = Path(raw_p).expanduser().resolve()
        if not target.exists():
            sys.stderr.write(f"[WARN] Path does not exist: {target}\n")
            continue

        files_to_scan = [target] if target.is_file() else sorted(target.rglob("*"))
        for fpath in files_to_scan:
            if not fpath.is_file():
                continue
            ext = fpath.suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            if any(part.startswith(".") for part in fpath.parts):
                continue

            raw_text = ""
            if ext in {".tex", ".sty", ".bib", ".md", ".txt"}:
                try:
                    raw_text = fpath.read_text(encoding="utf-8", errors="replace")
                except Exception as exc:
                    sys.stderr.write(f"[WARN] Could not read {fpath}: {exc}\n")
                    continue
            elif ext == ".docx":
                raw_text = extract_text_from_docx(fpath)
            elif ext == ".pdf":
                raw_text = extract_text_from_pdf(fpath)

            doc_type = classify_document(fpath, raw_text)
            category_counts[doc_type] += 1
            records.append(
                {
                    "path": str(fpath),
                    "filename": fpath.name,
                    "extension": ext,
                    "category": doc_type,
                    "size_bytes": fpath.stat().st_size,
                    "char_count": len(raw_text),
                }
            )

    manifest = {
        "input_paths": [str(Path(p).expanduser().resolve()) for p in args.paths],
        "total_files": len(records),
        "category_counts": dict(category_counts),
        "files": records,
    }

    out_path = Path(args.output).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Success! Ingested {len(records)} files. Manifest written to: {out_path}")
    return 0


def parse_latex_macros(tex: str) -> List[Dict[str, Any]]:
    """Extract custom macro definitions from LaTeX source."""
    macros: List[Dict[str, Any]] = []
    patterns = [
        (
            "newcommand",
            re.compile(
                r"\\(?:newcommand|renewcommand|providecommand)\*?\{\\([a-zA-Z]+)\}(?:\[(\d+)\])?(?:\[[^\]]*\])?\{([^\n]+)\}"
            ),
        ),
        (
            "DeclareMathOperator",
            re.compile(r"\\DeclareMathOperator\*?\{\\([a-zA-Z]+)\}\{([^\n]+)\}"),
        ),
        (
            "def",
            re.compile(r"\\def\\([a-zA-Z]+)\{([^\n]+)\}"),
        ),
    ]
    for kind, pat in patterns:
        for match in pat.finditer(tex):
            if kind == "newcommand":
                name, nargs, body = match.group(1), match.group(2) or "0", match.group(3)
            else:
                name, nargs, body = match.group(1), "0", match.group(2)
            macros.append(
                {
                    "kind": kind,
                    "name": f"\\{name}",
                    "nargs": int(nargs),
                    "body": body.strip(),
                    "raw": match.group(0).strip(),
                }
            )
    return macros


def cmd_extract_latex(args: argparse.Namespace) -> int:
    """Extract LaTeX macros, theorem environments, and package usage from corpus."""
    manifest_path = Path(args.manifest).expanduser().resolve()
    if not manifest_path.exists():
        sys.stderr.write(f"[ERROR] Manifest file not found: {manifest_path}\n")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    macro_map: Dict[str, Dict[str, Any]] = {}
    macro_usage: Counter = Counter()
    env_counts: Counter = Counter()
    packages: Counter = Counter()
    remark_intros: List[str] = []

    tex_files = [
        f for f in manifest.get("files", []) if f.get("extension") in {".tex", ".sty"}
    ]

    for item in tex_files:
        fpath = Path(item["path"])
        if not fpath.exists():
            continue
        raw = fpath.read_text(encoding="utf-8", errors="replace")
        cleaned = strip_latex_comments(raw)

        # Packages
        for pkg_match in re.finditer(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}", cleaned):
            for pkg in pkg_match.group(1).split(","):
                packages[pkg.strip()] += 1

        # Macros
        for m in parse_latex_macros(cleaned):
            mname = m["name"]
            if mname not in macro_map:
                macro_map[mname] = m
            macro_usage[mname] += 1

        # Environments
        for env_match in re.finditer(r"\\begin\{([a-zA-Z*]+)\}", cleaned):
            env_counts[env_match.group(1)] += 1

        # Remark openings
        for rem_match in re.finditer(
            r"\\begin\{remark\}(?:\[[^\]]*\])?\s*([^\n]{20,220})", cleaned, re.IGNORECASE
        ):
            remark_intros.append(rem_match.group(1).strip())

    # Count actual macro invocations across all .tex files
    for item in tex_files:
        fpath = Path(item["path"])
        if not fpath.exists():
            continue
        cleaned = strip_latex_comments(fpath.read_text(encoding="utf-8", errors="replace"))
        for mname in macro_map:
            hits = len(re.findall(re.escape(mname) + r"(?![a-zA-Z])", cleaned))
            macro_usage[mname] += hits

    sorted_macros = sorted(
        [
            {**info, "usage_count": macro_usage[name]}
            for name, info in macro_map.items()
        ],
        key=lambda x: x["usage_count"],
        reverse=True,
    )

    profile = {
        "tex_files_analyzed": len(tex_files),
        "top_packages": dict(packages.most_common(40)),
        "environment_counts": dict(env_counts.most_common(40)),
        "macros": sorted_macros,
        "sample_remark_openings": remark_intros[:25],
    }

    out_path = Path(args.output).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(profile, indent=2), encoding="utf-8")
    print(f"Success! Extracted {len(sorted_macros)} macros from {len(tex_files)} files to: {out_path}")
    return 0


def clean_prose_for_sentences(text: str, is_tex: bool = True) -> List[str]:
    """Convert raw LaTeX or Markdown into clean prose sentences for stylometric analysis."""
    if is_tex:
        text = strip_latex_comments(text)
        # Extract body if \begin{document} exists
        doc_match = re.search(
            r"\\begin\{document\}(.*?)\\end\{document\}", text, re.DOTALL
        )
        if doc_match:
            text = doc_match.group(1)
        # Replace display math with a placeholder token so sentence punctuation stays intact
        text = re.sub(
            r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?)\}.*?\\end\{\1\}",
            " [DISPLAY_EQ] ",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(r"\\\[.*?\\\]", " [DISPLAY_EQ] ", text, flags=re.DOTALL)
        text = re.sub(r"\$\$.*?\$\$", " [DISPLAY_EQ] ", text, flags=re.DOTALL)
        # Replace inline math with a single token
        text = re.sub(r"\$[^$]+\$", "[MATH]", text)
        # Remove structural commands
        text = re.sub(r"\\(?:section|subsection|subsubsection|paragraph|caption|label|ref|eqref|cite|citep|citet)\*?\{[^}]*\}", " ", text)
        text = re.sub(r"\\begin\{[^}]+\}|\\end\{[^}]+\}", " ", text)
        text = re.sub(r"\\[a-zA-Z]+\*?\{([^}]*)\}", r"\1", text)
        text = re.sub(r"\\[a-zA-Z]+", " ", text)

    # Split into paragraphs and sentences
    raw_sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z\[])", re.sub(r"\s+", " ", text))
    sentences = []
    for s in raw_sentences:
        s_clean = s.strip()
        words = s_clean.split()
        if 4 <= len(words) <= 120:
            sentences.append(s_clean)
    return sentences


def split_into_sections(text: str, is_tex: bool = True) -> Dict[str, str]:
    """Split a document into canonical academic sections."""
    sections: Dict[str, List[str]] = defaultdict(list)
    if is_tex:
        text = strip_latex_comments(text)
        abs_match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.DOTALL)
        if abs_match:
            sections["abstract"].append(abs_match.group(1))

        sec_pattern = re.compile(r"\\section\*?\{([^}]+)\}")
        matches = list(sec_pattern.finditer(text))
        for idx, m in enumerate(matches):
            title = m.group(1).lower()
            start = m.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            body = text[start:end]
            if "intro" in title:
                sections["introduction"].append(body)
            elif any(k in title for k in ("formul", "constitut", "theor", "govern", "model", "framework", "kinemat")):
                sections["formulation"].append(body)
            elif any(k in title for k in ("numer", "examp", "verif", "valid", "experim", "result", "bench")):
                sections["numerical_examples"].append(body)
            elif any(k in title for k in ("conclu", "summar", "discuss", "closing")):
                sections["conclusion"].append(body)
            elif any(k in title for k in ("thrust", "task", "object", "approach", "method", "plan")):
                sections["proposal_technical"].append(body)
            else:
                sections["other"].append(body)
    else:
        sections["full_text"].append(text)

    return {k: "\n\n".join(v) for k, v in sections.items()}


def compute_text_metrics(sentences: List[str], raw_text: str) -> Dict[str, Any]:
    """Compute sentence length statistics, transition frequencies, and voice markers."""
    if not sentences:
        return {"sentence_count": 0}

    lengths = [len(s.split()) for s in sentences]
    transitions: Counter = Counter()
    for s in sentences:
        for phrase in TRANSITION_PHRASES:
            if s.startswith(phrase) or s.lower().startswith(phrase.lower()):
                transitions[phrase] += 1

    post_eq_counts: Counter = Counter()
    for match in re.finditer(
        r"\\end\{(?:equation\*?|align\*?|gather\*?)\}\s*([a-zA-Z]+(?:\s+[a-zA-Z]+)?)",
        raw_text,
    ):
        token = match.group(1).strip()
        for starter in POST_EQUATION_STARTERS:
            if token.startswith(starter):
                post_eq_counts[starter] += 1

    all_words = " ".join(sentences).lower().split()
    total_words = max(len(all_words), 1)
    we_count = sum(1 for w in all_words if w in {"we", "our", "us"})
    passive_hits = len(
        re.findall(
            r"\b(?:is|are|was|were|be|been|being)\s+[a-z]+ed\b",
            " ".join(sentences).lower(),
        )
    )

    buckets = {
        "short_lt_15": round(sum(1 for l in lengths if l < 15) / len(lengths), 3),
        "medium_15_to_30": round(sum(1 for l in lengths if 15 <= l <= 30) / len(lengths), 3),
        "complex_31_to_45": round(sum(1 for l in lengths if 31 <= l <= 45) / len(lengths), 3),
        "long_gt_45": round(sum(1 for l in lengths if l > 45) / len(lengths), 3),
    }

    return {
        "sentence_count": len(sentences),
        "word_count": total_words,
        "sentence_length_mean": round(statistics.mean(lengths), 2),
        "sentence_length_median": round(statistics.median(lengths), 2),
        "sentence_length_stdev": round(statistics.stdev(lengths), 2) if len(lengths) > 1 else 0.0,
        "sentence_length_buckets": buckets,
        "first_person_plural_per_1k_words": round(we_count * 1000.0 / total_words, 2),
        "passive_markers_per_1k_words": round(passive_hits * 1000.0 / total_words, 2),
        "top_transitions": dict(transitions.most_common(20)),
        "post_equation_starters": dict(post_eq_counts.most_common(10)),
    }


def cmd_analyze_style(args: argparse.Namespace) -> int:
    """Analyze corpus stylometrics across document categories and canonical sections."""
    manifest_path = Path(args.manifest).expanduser().resolve()
    if not manifest_path.exists():
        sys.stderr.write(f"[ERROR] Manifest file not found: {manifest_path}\n")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_category_sentences: Dict[str, List[str]] = defaultdict(list)
    by_category_raw: Dict[str, List[str]] = defaultdict(list)
    by_section_sentences: Dict[str, List[str]] = defaultdict(list)
    by_section_raw: Dict[str, List[str]] = defaultdict(list)

    for item in manifest.get("files", []):
        cat = item.get("category", "journal_manuscript")
        if cat in {"bibliography", "macro_package"}:
            continue
        fpath = Path(item["path"])
        if not fpath.exists():
            continue
        ext = item.get("extension", "")
        if ext == ".tex":
            raw = fpath.read_text(encoding="utf-8", errors="replace")
            is_tex = True
        elif ext == ".docx":
            raw = extract_text_from_docx(fpath)
            is_tex = False
        elif ext == ".pdf":
            raw = extract_text_from_pdf(fpath)
            is_tex = False
        else:
            raw = fpath.read_text(encoding="utf-8", errors="replace")
            is_tex = False

        if not raw.strip():
            continue

        sents = clean_prose_for_sentences(raw, is_tex=is_tex)
        by_category_sentences[cat].extend(sents)
        by_category_raw[cat].append(raw)

        sec_map = split_into_sections(raw, is_tex=is_tex)
        for sec_name, sec_body in sec_map.items():
            sec_sents = clean_prose_for_sentences(sec_body, is_tex=is_tex)
            by_section_sentences[sec_name].extend(sec_sents)
            by_section_raw[sec_name].append(sec_body)

    category_profiles = {
        cat: compute_text_metrics(sents, "\n".join(by_category_raw[cat]))
        for cat, sents in by_category_sentences.items()
    }
    section_profiles = {
        sec: compute_text_metrics(sents, "\n".join(by_section_raw[sec]))
        for sec, sents in by_section_sentences.items()
    }

    output_data = {
        "files_analyzed": len(manifest.get("files", [])),
        "by_category": category_profiles,
        "by_section": section_profiles,
    }

    out_path = Path(args.output).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"Success! Style profile written to: {out_path}")
    return 0


def cmd_compare_drafts(args: argparse.Namespace) -> int:
    """Compare an early student draft against Prof. Sun's revised version."""
    before_path = Path(args.before).expanduser().resolve()
    after_path = Path(args.after).expanduser().resolve()
    if not before_path.exists() or not after_path.exists():
        sys.stderr.write("[ERROR] Both --before and --after files must exist.\n")
        return 1

    before_raw = before_path.read_text(encoding="utf-8", errors="replace")
    after_raw = after_path.read_text(encoding="utf-8", errors="replace")

    before_sents = clean_prose_for_sentences(
        before_raw, is_tex=(before_path.suffix.lower() == ".tex")
    )
    after_sents = clean_prose_for_sentences(
        after_raw, is_tex=(after_path.suffix.lower() == ".tex")
    )

    matcher = difflib.SequenceMatcher(None, before_sents, after_sents)
    replacements: List[Dict[str, Any]] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "replace":
            replacements.append(
                {
                    "before": " ".join(before_sents[i1:i2]),
                    "after": " ".join(after_sents[j1:j2]),
                }
            )

    report = {
        "before_file": str(before_path),
        "after_file": str(after_path),
        "before_metrics": compute_text_metrics(before_sents, before_raw),
        "after_metrics": compute_text_metrics(after_sents, after_raw),
        "replacement_count": len(replacements),
        "sample_transformations": replacements[:30],
    }

    out_path = Path(args.output).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Success! Draft comparison written to: {out_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Corpus Analyzer for Prof. WaiChing Sun's Writing Skill."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="Scan and classify corpus files.")
    p_ingest.add_argument(
        "--paths",
        nargs="+",
        required=True,
        help="One or more local directory or file paths to scan.",
    )
    p_ingest.add_argument(
        "--output",
        required=True,
        help="Output JSON manifest file path.",
    )
    p_ingest.set_defaults(func=cmd_ingest)

    p_latex = sub.add_parser(
        "extract-latex", help="Extract LaTeX macros and environments from manifest."
    )
    p_latex.add_argument("--manifest", required=True, help="Input manifest JSON.")
    p_latex.add_argument("--output", required=True, help="Output LaTeX profile JSON.")
    p_latex.set_defaults(func=cmd_extract_latex)

    p_style = sub.add_parser(
        "analyze-style", help="Compute section and category stylometrics from manifest."
    )
    p_style.add_argument("--manifest", required=True, help="Input manifest JSON.")
    p_style.add_argument("--output", required=True, help="Output style profile JSON.")
    p_style.set_defaults(func=cmd_analyze_style)

    p_diff = sub.add_parser(
        "compare-drafts",
        help="Compare a student rough draft against Prof. Sun's revised version.",
    )
    p_diff.add_argument("--before", required=True, help="Path to student/initial draft.")
    p_diff.add_argument("--after", required=True, help="Path to revised final version.")
    p_diff.add_argument("--output", required=True, help="Output JSON diff report.")
    p_diff.set_defaults(func=cmd_compare_drafts)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
