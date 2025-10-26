from github import Github
import os
import json
from dotenv import load_dotenv

# === 1️⃣ Load token from .env ===
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise ValueError("❌ GitHub token not found. Please add GITHUB_TOKEN to your .env file.")

# === 2️⃣ Connect to GitHub ===
g = Github(TOKEN)

# === 3️⃣ Define search keywords ===
keywords = [
    "debug",
    "traceback",
    "logging",
    "exception handling",
    "error handling",
    "try except",
    "fix bug",
    "assert"
]

# === 4️⃣ Create output folder to save results ===
os.makedirs("collected_repos", exist_ok=True)
results_file = os.path.join("collected_repos", "python_debug_repos.jsonl")

# === 5️⃣ Search and save results ===
with open(results_file, "w", encoding="utf-8") as f:
    for keyword in keywords:
        print(f"🔍 Searching for Python repositories with: {keyword}")
        repos = g.search_repositories(query=f"{keyword} language:Python stars:>50")

        for repo in repos[:10]:  # limit results for testing
            repo_info = {
                "name": repo.full_name,
                "url": repo.html_url,
                "stars": repo.stargazers_count,
                "description": repo.description,
                "keyword": keyword
            }
            f.write(json.dumps(repo_info) + "\n")
            print(f"📦 {repo.full_name} ({repo.stargazers_count}⭐)")

print(f"\n✅ Done! Results saved to: {results_file}")