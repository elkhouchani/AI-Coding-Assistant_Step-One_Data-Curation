import json
from pathlib import Path

# === 1️⃣ Paths ===
RAW_FILE = Path("../data/curated/debug_code.jsonl")   # your extracted file
CURATED_FILE = Path("../data/curated/debugging_dataset.jsonl")  # final output

# === 2️⃣ Keywords to detect debug code ===
DEBUG_KEYWORDS = [
    "debug", "traceback", "logger", "logging", "exception", "try:", "except",
    "assert", "raise", "print(", "error", "warning"
]

# === 3️⃣ Helper: check if a line is debug-related ===
def is_debug_line(line: str) -> bool:
    return any(kw in line.lower() for kw in DEBUG_KEYWORDS)

# === 4️⃣ Process each raw code snippet ===
def process_snippet(snippet: dict):
    code_lines = snippet["code"].splitlines()
    
    # Keep only lines containing debug keywords
    debug_lines = [line for line in code_lines if is_debug_line(line)]
    
    if not debug_lines:
        return None  # skip if no debug lines found

    # Optionally, you can take the whole code as input or just the debug lines
    # For now, input = debug lines, output = full code (or cleaned code)
    return {
        "task": "debugging",
        "input": "\n".join(debug_lines),
        "output": snippet["code"],  # or cleaned version
        "metadata": {
            "language": "python",
            "line_count": len(code_lines)
        }
    }

# === 5️⃣ Read raw file and create curated dataset ===
curated_snippets = []

with open(RAW_FILE, "r", encoding="utf-8") as f_in:
    for line in f_in:
        raw_snippet = json.loads(line)
        curated = process_snippet(raw_snippet)
        if curated:
            curated_snippets.append(curated)

# === 6️⃣ Save curated JSONL ===
with open(CURATED_FILE, "w", encoding="utf-8") as f_out:
    for snippet in curated_snippets:
        f_out.write(json.dumps(snippet) + "\n")

print(f"✅ Curated dataset saved! Total snippets: {len(curated_snippets)}")
