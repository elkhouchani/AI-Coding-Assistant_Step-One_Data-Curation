# 🧠 Debugging Dataset — AI Code Assistant
## 📄 Overview
This dataset was curated as part of our project on **AI Code Assistant**, focusing specifically on the **debugging** task.

It contains Python code snippets extracted from real public repositories, filtered and cleaned to represent typical debugging-related logic (error handling, logging, assertions, exceptions, etc.).

## 🎯 Objective

The goal of this phase was to:

- Collect open-source Python repositories related to debugging and error handling.
- Apply license and security checks to ensure compliance.
- Extract code snippets that illustrate debugging behavior (e.g., exception handling, logging, assertions).
- Clean and structure the data into a training-ready format suitable for fine-tuning code models on the debugging task.

## ⚙️ Methodology
### 1- Repository Collection

- Used GitHub’s API to search for repositories containing debugging-related keywords such as:
```
"debug", "traceback", "logger", "logging", "exception", "try:", "except", "assert", "raise", "error", "warning"

```
- Only repositories written in Python were collected.
- The results were stored in a JSONL file:
```
data/raw/collected_repos/debug_code.jsonl
```
### 2- License & Security Filtering

A dedicated script license_security.py:

- Checked each repository’s license type (MIT, BSD, Apache, etc.).
- Quarantined those that didn’t match allowed licenses listed in configs/tiny.yaml.
- Generated an Excel report:
```
reports/quarantine.xlsx
```
### 3- Code Extraction

Using the script extract_debug_code.py, each valid repository was:

- Cloned temporarily.
- Scanned recursively for .py files.
- Filtered to keep only files containing the defined debugging keywords.
- Extracted snippets were saved in:
```
data/curated/debug_code.jsonl
```

### 4- Data Cleaning and Structuring

A separate cleaning script standardized the data format and ensured uniformity across all tasks.

Each entry follows this JSONL structure:
```
{
  "task": "debugging",
  "input": "<buggy or incomplete debugging-related code>",
  "output": "<corrected or improved version of the same code>"
}
```
Example:
```
{
  "task": "debugging",
  "input": "try:\n    x = 1 / 0\nprint('Done')",
  "output": "try:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    print('Error: division by zero')\nprint('Done')"
}
```

### 5- Data Validation

A final validation script (validate_jsonl.py) ensured:
✅ All lines are valid JSON
✅ No empty fields (input/output)
✅ Consistent structure across entries
Validation Results:
```
📦 Total lines: 550  
✅ Valid JSON lines: 550  
⚠️ Empty inputs: 0  
⚠️ Empty outputs: 0  
❌ Invalid JSON lines: 0
```

## 📊 Dataset Summary
| Metric               | Value                     |
| -------------------- | ------------------------- |
| Programming language | Python                    |
| Total samples        | 550                       |
| Task type            | Debugging                 |
| Data format          | JSONL (UTF-8)             |
| Fields               | `task`, `input`, `output` |
| License compliance   | 100% verified             |
| Validation status    | ✅ Passed                  |


## 💡 Outcome

This curated dataset can now be integrated with other task datasets (e.g., refactoring, code completion, translation) to train a multi-task code model capable of:

- Detecting and correcting bugs.
- Understanding debugging patterns.
- Generating reliable error-handling logic.