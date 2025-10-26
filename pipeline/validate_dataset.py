import json
from pathlib import Path

# === 1️⃣ Paths ===
DATA_FILE = Path("../data/curated/debugging_clean.jsonl")

# === 2️⃣ Counters and checks ===
total = 0
valid = 0
invalid_lines = []
empty_inputs = 0
empty_outputs = 0

print(f"🔍 Checking dataset: {DATA_FILE}")

# === 3️⃣ Validate JSON lines ===
with open(DATA_FILE, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        total += 1
        try:
            item = json.loads(line)
            if not item.get("input"):
                empty_inputs += 1
            if not item.get("output"):
                empty_outputs += 1
            valid += 1
        except json.JSONDecodeError:
            invalid_lines.append(i)

# === 4️⃣ Display summary ===
print("\n✅ Validation Report")
print("--------------------")
print(f"📦 Total lines: {total}")
print(f"✅ Valid JSON lines: {valid}")
print(f"⚠️ Empty inputs: {empty_inputs}")
print(f"⚠️ Empty outputs: {empty_outputs}")
print(f"❌ Invalid JSON lines: {len(invalid_lines)}")

if invalid_lines:
    print("\n❗ Problematic line numbers:")
    print(invalid_lines)
else:
    print("\n🎯 All lines are valid JSON!")

# === 5️⃣ Quick sanity check: show one example ===
print("\n📖 Example record:")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    for _ in range(1):
        print(json.dumps(json.loads(f.readline()), indent=2))
