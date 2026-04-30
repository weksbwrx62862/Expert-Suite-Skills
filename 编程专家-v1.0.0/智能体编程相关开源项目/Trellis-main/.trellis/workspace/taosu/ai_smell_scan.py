#!/usr/bin/env python3
"""
AI-smell scanner for prose.

Catches the common LLM writing tics we've been cleaning up manually:
reversal patterns (isn't X, it's Y), formal transitions (Conversely, Moreover),
meta-narration filler (Let me zoom out), and other signatures of ChatGPT-style
writing.

Usage:
    python3 ai_smell_scan.py <file.md>
    python3 ai_smell_scan.py <file.md> --only HIGH
    python3 ai_smell_scan.py <file.md> --quiet   # summary only

Severity:
    HIGH    — near-certain AI tic, almost always worth fixing
    MEDIUM  — likely tic but has legitimate natural uses, review case-by-case
    LOW     — weak signal, often false-positive, skim only
"""

import argparse
import re
import sys
from pathlib import Path


# (name, severity, regex, description)
# Regexes are matched case-insensitive. All patterns are intended to run
# against individual lines (one paragraph per line in our Markdown).
PATTERNS = [
    # ========================================================================
    # REVERSAL FAMILY — the biggest AI tic
    # "not X, it's Y" / "don't X, do Y" / "never X — it was Y" / etc.
    # ========================================================================

    ("reversal:isnt-its", "HIGH",
     r"\b(is|was|are|were)n'?t\b[^.!?\n]{1,100}?\bit'?s\b",
     "isn't X, it's Y"),

    ("reversal:this-isnt-this-is", "HIGH",
     r"\bthis (is|was)n'?t\b[^.!?\n]{1,80}?[.!?]\s+this\s+(is|was)\b",
     "This isn't X. This is Y."),

    ("reversal:not-about-its-about", "HIGH",
     r"\bit'?s not about\b",
     "It's not about X, it's about Y"),

    ("reversal:not-a-bug", "HIGH",
     r"\bisn'?t a bug[,\s—-]+it'?s\b",
     "This isn't a bug — it's a feature"),

    # AI tic: same-subject reversal ("You don't X. You Y." / "We don't X. We Y.")
    # Natural prose: different-subject or 3rd-person description ("Judges don't X. They Y.")
    # We only catch the same-subject reversal because that's the LLM signature.
    ("reversal:you-dont-you-do", "HIGH",
     r"\byou don'?t\b[^.!?\n]{3,80}[.!?]\s+you\s+\w+",
     "You don't X. You Y. (same-subject reversal)"),

    ("reversal:we-dont-we-do", "HIGH",
     r"\bwe don'?t\b[^.!?\n]{3,80}[.!?]\s+we\s+\w+",
     "We don't X. We Y. (same-subject reversal)"),

    ("reversal:i-dont-i-do", "HIGH",
     r"\bi don'?t\b[^.!?\n]{3,80}[.!?]\s+i\s+\w+",
     "I don't X. I Y. (same-subject reversal)"),

    ("reversal:it-doesnt-it-does", "HIGH",
     r"\bit doesn'?t\b[^.!?\n]{3,80}[.!?]\s+it\s+\w+",
     "It doesn't X. It Y. (same-subject reversal)"),

    ("reversal:you-dont-need-you-need", "HIGH",
     r"\byou don'?t need to\b[^.!?\n]{1,80}?[—-]\s*you (need|have) to\b",
     "You don't need X — you need Y"),

    ("reversal:less-about-more-about", "HIGH",
     r"\bless about\b[^.!?\n]{1,100}?\bmore about\b",
     "less about X, more about Y"),

    ("reversal:never-was", "HIGH",
     r"\b(was|were) never\b[^.!?\n]{1,80}?[—-]\s*(it|they) (was|were)\b",
     "was never X — it was Y"),

    ("reversal:not-x-but-y", "MEDIUM",
     r"\bnot\s+[\w]+(?:\s+\w+){0,5}?,\s+but\s+\w+",
     "not X, but Y"),

    ("reversal:not-just-but", "MEDIUM",
     r"\bnot just\b[^.!?\n]{1,60}?\bbut\b",
     "not just X, but Y"),

    ("reversal:instead-of-x-y", "MEDIUM",
     r"\binstead of\b",
     "instead of X, Y"),

    ("reversal:rather-than", "MEDIUM",
     r"\brather than\b",
     "X rather than Y"),

    ("reversal:not-the-other-way", "MEDIUM",
     r"\bnot the other way around\b",
     "not the other way around (tail contrast)"),

    ("reversal:not-x-not-y", "MEDIUM",
     r"\bnot\s+\w+,\s+not\s+\w+",
     "Not X, not Y. [positive]"),

    ("reversal:it-also-works", "MEDIUM",
     r"\bit also (works|applies|holds|fits)\b",
     "X works as A. It also works as B"),

    # ========================================================================
    # META-NARRATION FILLER — "Let me X" and cousins
    # ========================================================================

    ("filler:let-me-meta", "HIGH",
     r"\blet me\s+(zoom|push|paint|explain|clarify|be\s+clear|walk\s+you|take\s+you|tell\s+you|break\s+this|unpack|dig)\b",
     "Let me X (meta-narration)"),

    ("filler:the-lesson-is-this", "HIGH",
     r"\bthe\s+(biggest|main|real|most\s+important|core|key)\s+(lesson|takeaway|insight|point)\b.{0,40}\bis\s+(this|that)\b",
     "The biggest lesson is this:"),

    ("filler:heres-the-thing", "MEDIUM",
     r"\bhere'?s the (thing|truth|kicker|catch|reality|point)\b",
     "here's the thing"),

    ("filler:heres-what", "MEDIUM",
     r"\bhere'?s what (i|you|we)\b",
     "here's what I/you/we..."),

    ("filler:its-worth-noting", "HIGH",
     r"\bit'?s worth (noting|mentioning|remembering|highlighting)\b",
     "it's worth noting"),

    ("filler:its-important-to", "MEDIUM",
     r"\bit'?s important to (note|remember|understand|mention|realize)\b",
     "it's important to X"),

    ("filler:at-the-end-of-the-day", "HIGH",
     r"\bat the end of the day\b",
     "at the end of the day"),

    ("filler:more-importantly", "MEDIUM",
     r"\bmore importantly\b",
     "more importantly"),

    ("filler:in-other-words", "MEDIUM",
     r"\bin other words\b",
     "in other words"),

    ("filler:at-its-core", "MEDIUM",
     r"\bat its core\b",
     "at its core"),

    ("filler:when-all-is-said", "HIGH",
     r"\bwhen all is said and done\b",
     "when all is said and done"),

    ("filler:the-truth-is", "MEDIUM",
     r"\bthe truth is\b",
     "the truth is"),

    # ========================================================================
    # FORMAL TRANSITIONS — AI overuses these, humans rarely do in casual prose
    # ========================================================================

    ("formal:conversely", "HIGH", r"\bconversely\b", "Conversely"),
    ("formal:moreover", "HIGH", r"\bmoreover\b", "Moreover"),
    ("formal:furthermore", "HIGH", r"\bfurthermore\b", "Furthermore"),
    ("formal:additionally", "MEDIUM", r"\badditionally\b", "Additionally"),
    ("formal:essentially", "MEDIUM", r"\bessentially\b", "Essentially"),
    ("formal:fundamentally", "MEDIUM", r"\bfundamentally\b", "Fundamentally"),
    ("formal:ultimately", "LOW", r"\bultimately\b", "Ultimately"),
    ("formal:crucially", "MEDIUM", r"\bcrucially\b", "Crucially"),
    ("formal:notably", "MEDIUM", r"\bnotably\b", "Notably"),
    ("formal:indeed", "MEDIUM", r"\bindeed\b", "Indeed"),

    # ========================================================================
    # INTENSIFIERS & HEDGE WORDS — high false-positive, LOW severity
    # ========================================================================

    ("intensifier:truly", "LOW", r"\btruly\b", "truly"),
    ("intensifier:genuinely", "LOW", r"\bgenuinely\b", "genuinely"),
    ("intensifier:incredibly", "LOW", r"\bincredibly\b", "incredibly"),
    ("intensifier:absolutely", "LOW", r"\babsolutely\b", "absolutely"),
    ("intensifier:literally-filler", "LOW", r"\bliterally\b", "literally (often AI filler)"),
    ("intensifier:actually-filler", "LOW", r"\bactually\b", "actually (possible filler)"),

    # ========================================================================
    # TAUTOLOGIES / CLOSINGS that AI likes
    # ========================================================================

    ("closing:thats-just-how", "LOW",
     r"\bthat'?s just how\b",
     "that's just how X works"),

    ("closing:one-more-thing", "MEDIUM",
     r"\bone more thing\b",
     "one more thing"),

    # ========================================================================
    # QUANTIFIER CLICHÉS
    # ========================================================================

    ("cliche:night-and-day", "LOW",
     r"\bnight and day\b",
     "night and day (cliché)"),

    ("cliche:game-changer", "HIGH",
     r"\bgame[- ]chang(er|ing)\b",
     "game changer / game-changing"),

    ("cliche:in-todays-world", "HIGH",
     r"\bin today'?s (world|landscape|era)\b",
     "in today's world/landscape"),

    ("cliche:delve-into", "HIGH",
     r"\bdelve into\b",
     "delve into (famous ChatGPT tell)"),

    ("cliche:tapestry", "HIGH",
     r"\btapestry\b",
     "tapestry (famous ChatGPT tell)"),

    ("cliche:navigate-the", "MEDIUM",
     r"\bnavigate the (complex|intricate|nuanced|ever-changing)\b",
     "navigate the [complex] X"),

    ("cliche:testament-to", "HIGH",
     r"\ba testament to\b",
     "a testament to"),
]


def is_skippable(line: str) -> bool:
    """Skip code fences, headings, list markers, blockquotes, horizontal rules."""
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("```"):
        return True
    if stripped.startswith("#"):  # markdown heading
        return True
    if stripped.startswith("---") or stripped.startswith("==="):
        return True
    if stripped.startswith("|"):  # table row
        return True
    return False


def scan_file(path: Path, in_code_block: bool = False):
    text = path.read_text()
    lines = text.split("\n")
    findings = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track code fences
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if is_skippable(line):
            continue

        for name, severity, pattern, description in PATTERNS:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                findings.append({
                    "line": i,
                    "severity": severity,
                    "name": name,
                    "description": description,
                    "match": match.group(0),
                    "full_line": stripped,
                })

    return findings


SEVERITY_ORDER = ["HIGH", "MEDIUM", "LOW"]
SEVERITY_COLOR = {
    "HIGH": "\033[91m",    # red
    "MEDIUM": "\033[93m",  # yellow
    "LOW": "\033[90m",     # grey
}
RESET = "\033[0m"


def print_findings(findings, only=None, quiet=False, color=True):
    by_severity = {s: [] for s in SEVERITY_ORDER}
    for f in findings:
        by_severity[f["severity"]].append(f)

    if not quiet:
        for severity in SEVERITY_ORDER:
            if only and severity != only:
                continue
            items = by_severity[severity]
            if not items:
                continue
            col = SEVERITY_COLOR[severity] if color else ""
            print()
            print("=" * 72)
            print(f"  {col}{severity}{RESET if color else ''} — {len(items)} finding(s)")
            print("=" * 72)

            for f in items:
                snippet = f["full_line"]
                if len(snippet) > 160:
                    # Center the snippet around the match
                    idx = snippet.lower().find(f["match"].lower())
                    if idx >= 0:
                        start = max(0, idx - 60)
                        end = min(len(snippet), idx + len(f["match"]) + 60)
                        snippet = ("..." if start > 0 else "") + snippet[start:end] + ("..." if end < len(f["full_line"]) else "")

                print(f"\n  L{f['line']:<4} [{f['name']}]")
                print(f"        → {f['description']}")
                print(f"        Match:   \"{f['match']}\"")
                print(f"        Context: {snippet}")

    # Summary
    total = sum(len(v) for v in by_severity.values())
    print()
    print("=" * 72)
    print(f"  Summary: {total} total")
    for s in SEVERITY_ORDER:
        col = SEVERITY_COLOR[s] if color else ""
        print(f"    {col}{s}{RESET if color else ''}: {len(by_severity[s])}")
    print("=" * 72)


def main():
    ap = argparse.ArgumentParser(description="AI-smell scanner for prose.")
    ap.add_argument("file", type=Path, help="Markdown or text file to scan")
    ap.add_argument("--only", choices=SEVERITY_ORDER, help="Only show findings at this severity")
    ap.add_argument("--quiet", action="store_true", help="Summary only, skip individual findings")
    ap.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    args = ap.parse_args()

    if not args.file.exists():
        print(f"ERROR: {args.file} not found", file=sys.stderr)
        sys.exit(2)

    findings = scan_file(args.file)
    print_findings(findings, only=args.only, quiet=args.quiet, color=not args.no_color)

    # Exit code: 0 if clean, 1 if HIGH findings exist, 2 if only MEDIUM/LOW
    high = sum(1 for f in findings if f["severity"] == "HIGH")
    if high > 0:
        sys.exit(1)
    if findings:
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
