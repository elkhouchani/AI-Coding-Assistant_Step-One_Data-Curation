import os
import json
import subprocess
import tempfile
from pathlib import Path

# === Input: repos collected ===
INPUT_FILE = "../data/raw/collected_repos/python_debug_repos.jsonl"
OUTPUT_FILE = "../data/curated/bugfix_pairs.jsonl"

# Keywords that indicate bug fix commits
BUGFIX_KEYWORDS = ["fix", "bug", "error", "exception", "issue", "debug"]

def get_bugfix_commits(repo_path: Path):
    """Return commit hashes whose message contains bugfix keywords."""
    result = subprocess.run(
        ["git", "-C", str(repo_path), "log", "--pretty=format:%H %s"],
        capture_output=True, text=True
    )
    commits = []
    for line in result.stdout.splitlines():
        if any(k in line.lower() for k in BUGFIX_KEYWORDS):
            commit_hash = line.split()[0]
            commits.append(commit_hash)
    return commits

def extract_diff_pair(repo_path: Path, commit_hash: str):
    """Extract the before/after code for files changed in this commit."""
    result = subprocess.run(
        ["git", "-C", str(repo_path), "diff", f"{commit_hash}~1", commit_hash, "--", "*.py"],
        capture_output=True, text=True
    )
    diff_text = result.stdout
    if not diff_text.strip():
        return None

    return {
        "repo": repo_path.name,
        "commit": commit_hash,
        "diff": diff_text
    }

def process_repo(repo_url: str):
    """Clone repo and extract bug-fix pairs."""
    temp_dir = tempfile.mkdtemp()
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = Path(temp_dir) / repo_name

    subprocess.run(["git", "clone", repo_url, str(repo_path)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    commits = get_bugfix_commits(repo_path)
    pairs = []

    for commit in commits:
        pair = extract_diff_pair(repo_path, commit)
        if pair:
            pairs.append(pair)

    return pairs

def main():
    os.makedirs("../data/curated", exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:

        for line in f_in:
            repo = json.loads(line)
            print(f"🔍 Scanning {repo['name']} for bug fix commits...")
            try:
                pairs = process_repo(repo["url"])
                for p in pairs:
                    f_out.write(json.dumps(p) + "\n")
            except Exception as e:
                print(f"⚠️ Failed to process {repo['name']}: {e}")

    print(f"\n✅ Done! Saved bug-fix pairs to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
