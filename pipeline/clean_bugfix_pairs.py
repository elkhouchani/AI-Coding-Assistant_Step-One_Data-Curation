import os
import re
import json
from pathlib import Path

INPUT_FILE = "../data/curated/bugfix_pairs.jsonl"
OUTPUT_FILE = "../data/curated/debugging_clean.jsonl"

def extract_code_from_diff(diff_text: str):
    """Split a diff into buggy (old) and fixed (new) code versions."""
    buggy_lines = []
    fixed_lines = []
    current_file = None

    for line in diff_text.splitlines():
        # Skip metadata lines
        if line.startswith(("diff --git", "index", "---", "+++", "@@")):
            continue

        if line.startswith("-"):
            buggy_lines.append(line[1:])
        elif line.startswith("+"):
            fixed_lines.append(line[1:])
        else:
            buggy_lines.append(line)
            fixed_lines.append(line)

    buggy_code = "\n".join(buggy_lines).strip()
    fixed_code = "\n".join(fixed_lines).strip()

    return buggy_code, fixed_code

def clean_code(code: str):
    """Simple cleaning: remove excessive blank lines & trailing spaces."""
    lines = [l.rstrip() for l in code.splitlines() if l.strip()]
    return "\n".join(lines)

def main():
    os.makedirs("../data/curated", exist_ok=True)
    count = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:

        for line in f_in:
            record = json.loads(line)
            diff = record.get("diff", "")
            if not diff:
                continue

            buggy, fixed = extract_code_from_diff(diff)
            if not buggy or not fixed or buggy == fixed:
                continue

            item = {
                "repo": record.get("repo"),
                "task": "code_debugging",
                "language": "python",
                "input": clean_code(buggy),
                "output": clean_code(fixed)
            }

            f_out.write(json.dumps(item) + "\n")
            count += 1

    print(f"✅ Cleaned {count} pairs → saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
