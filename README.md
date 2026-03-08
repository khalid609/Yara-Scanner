# Yara Scanner Project

This project is a Yara Scanner designed to scan files using Yara rules for malware detection and analysis. It includes functionalities for scanning files, applying Yara rules, generating reports, and organizing data in JSON format.

## Project Description

The Yara Scanner project is a tool for detecting and analyzing malware using Yara rules. It scans files, applies Yara rules to detect matches, and generates detailed reports. The project is structured to handle file scanning, Yara rule application, and report generation efficiently.

## File Descriptions

### execute.py
This is the main script that orchestrates the scanning process. It uses argument parsing to accept a path to scan and coordinates the file scanning, Yara rule application, and report generation.

### yara_scanner.py
This script handles the Yara rule scanning process. It loads Yara rules from JSON files, applies them to the files being scanned, and dumps the results into JSON files for alerts, errors, and files with no matches found.

### Report.py
This script is responsible for generating a detailed report from the scan results. It reads the JSON files containing scan results and generates a human-readable report.

### json_organizer.py
This script manages the paths and organization of JSON files used throughout the project. It provides methods to load and save data in JSON format.

### file_scanner.py
This script scans the specified directory for files and rules, and dumps the file paths into JSON files for further processing.

### ioc_automated_scanner.py
This script contains a class for extracting Indicators of Compromise (IOCs) such as file hashes.

## Requirements

- Python 3.x
- yara-python (Yara library for Python)
- json (for handling JSON data)
- os (for file and directory operations)
- argparse (for command-line argument parsing)
- hashlib (for calculating file hashes)
- datetime (for timestamping reports)

## Installation

1. **Prerequisites**: Ensure you have Python 3.x installed on your system.
2. **Clone the Repository**:
   ```bash
   git clone https://github.com/khalid609/YaraScanner.git

3. **Directory Structure**
	.
├── execute.py
├── json
│   ├── directory_content.json
│   ├── alert_results.json
│   ├── error_results.json
│   └── not_found_results.json



├── Report
│   └── (generated reports)



├── Script
│   ├── file_scanner.py
│   ├── ioc_automated_scanner.py
│   ├── json_organizer.py
│   ├── Report.py
│   └── yara_scanner.py
└── yara
    ├── rules
    └── rules.json


	
3. **how to use **
 - add your yara rule (.yar) inside 
	yara
    	├── rules
 - use: python execute.py -p /path/to/scan
 - you can find the result inside 
    	Report
│   	└── (generated reports)
	
