import os
import shutil
import yaml
import pandas as pd

# --- Load config file ---
config_path = os.path.join("configs", "tiny.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

raw_dir = os.path.join("data", "raw")
quarantine_dir = os.path.join("data", "quarantine")
report_path = os.path.join("reports", "quarantine.xlsx")

os.makedirs(quarantine_dir, exist_ok=True)
os.makedirs(os.path.dirname(report_path), exist_ok=True)

allowed_licenses = config["compliance"]["license_allow"]

def detect_license(repo_path):
    """Reads LICENSE file and tries to detect the license type."""
    license_path = os.path.join(repo_path, "LICENSE")
    if not os.path.exists(license_path):
        return None

    with open(license_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read().lower()

    if "mit" in text:
        return "MIT"
    elif "bsd" in text:
        return "BSD"
    elif "apache" in text:
        return "Apache-2.0"
    elif "creative commons" in text or "cc by" in text:
        return "CC-BY"
    else:
        return "Unknown"

# --- Load existing report if exists ---
if os.path.exists(report_path):
    df_existing = pd.read_excel(report_path)
    processed_repos = set(df_existing["repo"].tolist())
else:
    df_existing = pd.DataFrame()
    processed_repos = set()

# --- Process each repo in data/raw ---
records = []

for repo_name in os.listdir(raw_dir):
    repo_path = os.path.join(raw_dir, repo_name)
    if not os.path.isdir(repo_path):
        continue

    if repo_name in processed_repos:
        print(f"ℹ️ Skipping already processed repo: {repo_name}")
        continue

    license_type = detect_license(repo_path)
    decision = "keep"

    if license_type not in allowed_licenses:
        decision = "quarantine"
        shutil.move(repo_path, os.path.join(quarantine_dir, repo_name))
        print(f"❌ Quarantined: {repo_name} (License: {license_type})")
    else:
        print(f"✅ Kept: {repo_name} (License: {license_type})")

    records.append({
        "repo": repo_name,
        "license": license_type,
        "decision": decision
    })

# --- Write updated report ---
if not df_existing.empty:
    df = pd.concat([df_existing, pd.DataFrame(records)], ignore_index=True)
else:
    df = pd.DataFrame(records)

df.to_excel(report_path, index=False)

print("✅ License & security gating completed.")
print(f"Report saved to: {report_path}")
