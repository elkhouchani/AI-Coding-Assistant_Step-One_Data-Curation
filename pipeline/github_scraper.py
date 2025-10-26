import os
import requests
import yaml
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables (for your GitHub token)
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("⚠️ Missing GitHub token! Please add it to your .env file.")

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def search_repositories(query, max_repos=2):
    """Search public repositories on GitHub by query."""
    url = f"https://api.github.com/search/repositories?q={query}&per_page={max_repos}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    items = response.json().get("items", [])
    return items

def download_repo(repo_clone_url, dest_dir):
    """Clone the repository using Git."""
    from git import Repo
    repo_name = repo_clone_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(dest_dir, repo_name)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    print(f"📦 Downloading {repo_name} ...")
    Repo.clone_from(repo_clone_url, repo_path)
    print(f"✅ Done: {repo_path}")

def main():
    config = load_config("configs/tiny.yaml")
    github_conf = config["sources"]["github"]

    query = github_conf["query"]
    max_repos = github_conf["max_repos"]

    results = search_repositories(query, max_repos=max_repos)

    print(f"🔍 Found {len(results)} repositories.")

    for repo in tqdm(results, desc="Downloading repos"):
        download_repo(repo["clone_url"], "data/raw")

if __name__ == "__main__":
    main()
