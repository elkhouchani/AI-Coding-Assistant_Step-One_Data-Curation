import json, random
from pathlib import Path

INPUT_FILE = "../data/curated/debugging_clean.jsonl"
OUTPUT_FILE = "../data/curated/debugging_with_instructions.jsonl"

INSTRUCTIONS = [
    "Fix the bugs in the following code.",
    "Debug the following Python function.",
    "Identify and correct the errors in this code snippet.",
    "Find and fix issues in the provided script.",
    "Correct the mistakes in this piece of code.",
    "Make the following code run correctly by fixing its bugs.",
    "Review and repair the faulty code below.",
    "Locate and fix the problem in this code.",
    "Improve this script so it runs without errors.",
    "Analyze and correct the following buggy Python code.",
    "Inspect this code and correct all syntax and logic errors.",
    "Debug the following function to produce the correct output.",
    "Troubleshoot and fix all issues in this code snippet.",
    "Rewrite the code so that it executes without errors.",
    "Detect and correct any logical or runtime errors in this script.",
    "Ensure the following program runs successfully by fixing its bugs.",
    "Clean up and repair the code below to make it functional.",
    "Fix the issues preventing this Python code from running properly.",
    "Resolve any errors and make the provided code valid Python syntax.",
    "Examine the snippet and correct the buggy implementation."
]

input_path = Path(INPUT_FILE)
output_path = Path(OUTPUT_FILE)

with open(input_path, "r", encoding="utf-8") as fin, \
     open(output_path, "w", encoding="utf-8") as fout:

    for line in fin:
        try:
            data = json.loads(line)
            # Insert "instruction" as the first key
            data = {"instruction": random.choice(INSTRUCTIONS), **data}
            fout.write(json.dumps(data, ensure_ascii=False) + "\n")
        except json.JSONDecodeError:
            continue

print(f"✅ Instructions added successfully! Saved to: {output_path}")
