# 🔍 YARA File Scanner

> An automated file scanner that uses YARA rules to detect malware and suspicious files, extracts IOCs, collects file metadata, and generates a structured scan report.

---

## 📌 Overview

YARA File Scanner is a Python-based security tool that automates the process of scanning a directory of files against a set of YARA rules. It is designed for malware analysts, threat hunters, and cybersecurity students who want to automate static file analysis in a lab environment.

**What it does:**
- Recursively walks a target directory and collects all file paths
- Loads compiled YARA rules from a rules directory
- Matches every file against every rule
- Extracts SHA-256 hashes and full file metadata for matched files
- Outputs structured JSON results (alerts, errors, not found)
- Generates a human-readable `.txt` scan report

---

## 🏗️ Architecture

```
execute.py  (entry point)
    │
    ├── FileScanner        → walks target dir + rules dir → dumps to JSON
    │
    ├── YaraScanner        → loads rules JSON → matches files → dumps results
    │   └── Exteact_ioc    → computes SHA-256 hash per matched file
    │
    └── Report             → reads result JSONs → generates .txt report

JsonOrganizer              → centralized path manager (used by all modules)
```

---

## 📁 Project Structure

```
Project-2-YARA_SCANNER/
├── execute.py                  ← entry point
├── Script/
│   ├── file_scanner.py         ← directory walker
│   ├── yara_scanner.py         ← YARA matching engine
│   ├── ioc_automated_scanner.py← IOC extraction (hashing)
│   ├── json_organizer.py       ← centralized path manager
│   └── Report.py               ← report generator
├── yara/
│   ├── rules/                  ← place your .yar rule files here
│   └── rules.json              ← auto-generated index of rule paths
├── json/
│   ├── directory_content.json  ← auto-generated list of scanned files
│   ├── alert_results.json      ← matched files output
│   ├── error_results.json      ← scan errors output
│   └── not_found_results.json  ← clean files output
└── Report/
    └── scan_report_<timestamp>.txt  ← final report
```

---

## 📄 File Reference

| File | Role |
|---|---|
| `execute.py` | Entry point — orchestrates the full scan pipeline |
| `file_scanner.py` | Recursively collects file and rule paths, dumps to JSON |
| `yara_scanner.py` | Compiles and matches YARA rules against collected files |
| `ioc_automated_scanner.py` | Computes SHA-256 hash for each matched file |
| `json_organizer.py` | Manages all file/directory paths used across modules |
| `Report.py` | Reads JSON results and writes a formatted `.txt` report |

---

## 🔬 How It Works

### Step 1 — File Discovery (`FileScanner`)
Recursively walks the target path and the YARA rules directory using `os.walk`. Dumps two JSON files — one with all target file paths, one with all rule file paths.

### Step 2 — YARA Scanning (`YaraScanner`)
Loads the rule paths JSON, compiles each `.yar` file using `yara.compile()`, then matches every rule against every file. Results are split into three categories:

| Category | Description |
|---|---|
| `ALERT` | File matched one or more YARA rules |
| `NOT FOUND` | File scanned cleanly with no matches |
| `ERROR` | File could not be scanned (access error, corrupt file, etc.) |

### Step 3 — IOC Extraction (`Exteact_ioc`)
For each matched file, computes a **SHA-256** hash using chunked reading (4096-byte blocks) to handle large files safely.

### Step 4 — Metadata Collection
For every alert, the scanner collects full file metadata:

| Field | Detail |
|---|---|
| `size_bytes` | File size |
| `created_time` | Creation timestamp |
| `modified_time` | Last modification timestamp |
| `accessed_time` | Last access timestamp |
| `mode` | File permissions |
| `inode` | Filesystem inode |
| `device` | Device ID |

### Step 5 — Report Generation (`Report`)
Reads the three result JSON files and produces a timestamped `.txt` report with summary statistics, full alert details, clean file list, and error log.

---

## ⚙️ Setup

### Prerequisites

- Python **3.13** (recommended — 3.14 not yet supported by `yara-python`)
- `yara-python` library

### Install

```bash
git clone https://github.com/khalid609/Yara-Scanner.git
cd Yara-Scanner/Project-2-YARA_SCANNER
pip install yara-python
```

### Add your YARA rules

Place your `.yar` rule files inside:
```
yara/rules/
```

The scanner will automatically index them on first run.

---

## 🚀 Usage

### Step 1 — Add your YARA rules

Place your `.yar` rule files inside the rules directory:

```
yara/
└── rules/
    ├── ransomware.yar
    ├── trojan.yar
    └── suspicious_strings.yar
```

The scanner will automatically walk this folder, collect all rule file paths, and save them to `yara/rules.json`. That index file is then loaded by the YARA scanner to compile and run each rule against the target files.

> You do not need to edit `rules.json` manually — it is auto-generated every run.

---

### Step 2 — Run the scanner

```bash
python execute.py -p "C:\path\to\target\folder"
```

| Argument | Description |
|---|---|
| `-p` / `--path` | Path to the directory you want to scan |

### Example

```bash
python execute.py -p "C:\samples"
```

### How the two paths work together

```
yara/rules/          ← you put your .yar files here
      │
      ▼
yara/rules.json      ← auto-generated index of rule paths
      │
      ▼
YaraScanner          ← compiles each rule and matches against target files
      │
      ▼
-p "C:\samples"      ← the folder you pass at runtime — all files here get scanned
```

Every file in your target path is matched against every rule in `yara/rules/`. If a file triggers a rule it goes to `alert_results.json`. If not it goes to `not_found_results.json`.

---

### Output

```
[+] Scan files start
[+] Scan rules start
[+] Dumping files start
[+] Dumping rules start
[+][+] end operation 1 success
Loaded rule: ...\yara\rules\ransomware.yar
Loaded rule: ...\yara\rules\trojan.yar
Found 3 files with matches.
(Alerts) dumped to ...\json\alert_results.json
(Errors) dumped to ...\json\error_results.json
(Not found) results dumped to ...\json\not_found_results.json
Report generated and saved to: ...\Report\scan_report_20250519_143022.txt
```

---

## 📊 Output Format

### alert_results.json

```json
[
  {
    "[ALERT]": "Malware detected",
    "matches found": "C:\\samples\\suspicious.exe",
    "hash": "e3b0c44298fc1c149afb...",
    "Rules": ["Ransomware_Generic", "Suspicious_PE"],
    "metadata": {
      "size_bytes": 204800,
      "created_time": "Mon May 19 14:30:00 2025",
      "modified_time": "Mon May 19 14:30:00 2025"
    }
  }
]
```

### scan_report.txt

```
================================================================================
SCAN REPORT
Generated on: 2025-05-19 14:30:22
================================================================================

SUMMARY:
- Total Scans: 120
- Number of Errors: 2
- Number of Clear Files: 117

ALERTS:
[ALERT]: Malware detected
Matches Found: C:\samples\suspicious.exe
Hash: e3b0c44298fc1c149afb...
Rules Triggered:
  - Ransomware_Generic
...
```

---

## ⚠️ Known Limitations

| Issue | Detail |
|---|---|
| Python 3.14 | `yara-python` has no wheel for 3.14 yet — use Python 3.13 |
| AES mode | IOC extraction is currently SHA-256 only — MD5/SHA-1 not yet implemented |
| Single-threaded | Large directories may be slow — no parallel scanning yet |
| Rule compilation | Each rule is compiled separately per scan — no caching |

---

## 🛡️ What This Teaches

| Topic | Detail |
|---|---|
| YARA rule matching | How signature-based detection works |
| File metadata forensics | Timestamps, permissions, inode analysis |
| IOC extraction | Hashing files for threat intelligence |
| JSON-based pipelines | Passing structured data between scan stages |
| Report generation | Turning raw scan data into readable output |
| Directory traversal | Recursive file discovery with `os.walk` |

---

## 👤 Author

**Khalid** — Cybersecurity Student
GitHub: [@khalid609](https://github.com/khalid609)

---

## 📄 License

For educational and authorized security research use only.
See [LICENSE](LICENSE) for details.
