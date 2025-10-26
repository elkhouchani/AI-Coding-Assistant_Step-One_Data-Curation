import os
import json
import re
import tempfile
import subprocess
from pathlib import Path

# === 1️⃣ Define base directory (project root) ===
BASE_DIR = Path(__file__).resolve().parents[1]  # Goes one level up from "pipeline/"

# === 2️⃣ Input / Output paths ===
INPUT_FILE = BASE_DIR / "data" / "raw" / "collected_repos" / "python_debug_repos.jsonl"
OUTPUT_FILE = BASE_DIR / "data" / "curated" / "debug_code.jsonl"


# === 2️⃣ Define keywords that indicate debugging-related code ===
DEBUG_KEYWORDS = [
    "debug", "traceback", "logger", "logging", "exception", "try:", "except",
    "assert", "raise", "print(", "error", "warning"
]

# === 3️⃣ Helper function: check if a line looks debugging-related ===
def is_debug_related(line: str) -> bool:
    return any(kw in line.lower() for kw in DEBUG_KEYWORDS)

# === 4️⃣ Function to clone repo (temporary folder) ===
def clone_repo(repo_url: str) -> Path | None:
    try:
        temp_dir = tempfile.mkdtemp()
        subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_dir],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return Path(temp_dir)
    except Exception as e:
        print(f"⚠️ Failed to clone {repo_url}: {e}")
        return None

# === 5️⃣ Extract .py files containing debugging code ===
def extract_debugging_code(repo_url: str):
    snippets = []
    repo_path = clone_repo(repo_url)
    if not repo_path:
        return snippets

    for py_file in repo_path.rglob("*.py"):
        try:
            with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if any(is_debug_related(line) for line in content.splitlines()):
                snippets.append({
                    "repo": repo_url,
                    "file": str(py_file),
                    "code": content
                })
        except Exception:
            continue

    return snippets

# === 6️⃣ Main processing ===
def main():
    os.makedirs("outputs", exist_ok=True)
    with open(INPUT_FILE, "r", encoding="utf-8") as f_in, \
        open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:

        for line in f_in:
            repo = json.loads(line)
            print(f"🔍 Extracting from {repo['name']} ...")
            code_snippets = extract_debugging_code(repo["url"])

            for snippet in code_snippets:
                f_out.write(json.dumps(snippet) + "\n")

    print(f"\n✅ Done! Saved dataset to outputs/{OUTPUT_FILE}")

if __name__ == "__main__":
    main()
