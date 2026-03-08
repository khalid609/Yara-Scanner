import json
from datetime import datetime
from Script.json_organizer import JsonOrganizer
import time
import os 

class Report:
    def __init__(self):
        _org = JsonOrganizer()
        self.alert = _org.get_alert_results_json_path()
        self.error = _org.get_error_results_json_path()
        self.clear = _org.get_not_found_results_json_path()
        self.report = _org.get_report_txt_path()

    def generate_scan_report(self, alerts_path, clear_path, errors_path, report_path):
        # Load JSON files, handle empty files gracefully
        try:
            with open(alerts_path, 'r', encoding='utf-8') as f:
                alerts = json.load(f)
        except json.JSONDecodeError:
            alerts = []

        try:
            with open(clear_path, 'r', encoding='utf-8') as f:
                clear_files = json.load(f)
        except json.JSONDecodeError:
            clear_files = []

        try:
            with open(errors_path, 'r', encoding='utf-8') as f:
                errors = json.load(f)
        except json.JSONDecodeError:
            errors = []

        # Calculate statistics
        total_scans = len(alerts) + len(clear_files) + len(errors)
        num_errors = len(errors)
        num_clear = len(clear_files)

        # Generate report
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("SCAN REPORT")
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 80 + "\n")

        # Summary
        report_lines.append("SUMMARY:")
        report_lines.append(f"- Total Scans: {total_scans}")
        report_lines.append(f"- Number of Errors: {num_errors}")
        report_lines.append(f"- Number of Clear Files: {num_clear}\n")

        # Alerts
        report_lines.append("ALERTS:")
        if alerts:
            for alert in alerts:
                report_lines.append(f"[ALERT]: {alert.get('[ALERT]', 'N/A')}")
                report_lines.append(f"Matches Found: {alert.get('matches found', 'N/A')}")
                report_lines.append(f"Hash: {alert.get('hash', 'N/A')}")
                report_lines.append("Rules Triggered:")
                for rule in alert.get('Rules', []):
                    report_lines.append(f"  - {rule}")
                report_lines.append("Metadata:")
                metadata = alert.get('metadata', {})
                report_lines.append(f"  - Size: {metadata.get('size_bytes', 'N/A')} bytes")
                report_lines.append(f"  - Created: {metadata.get('created_time', 'N/A')}")
                report_lines.append(f"  - Modified: {metadata.get('modified_time', 'N/A')}")
                report_lines.append(f"  - Accessed: {metadata.get('accessed_time', 'N/A')}")
                report_lines.append("-" * 80 + "\n")
        else:
            report_lines.append("No alerts found.\n")

        # Clear Files
        report_lines.append("CLEAR FILES:")
        if clear_files:
            for clear in clear_files:
                report_lines.append(f"No matches found: {clear.get('No matches found', 'N/A')}")
            report_lines.append("-" * 80 + "\n")
        else:
            report_lines.append("No clear files found.\n")

        # Errors
        report_lines.append("SCANNING ERRORS:")
        if errors:
            for error in errors:
                report_lines.append(f"Error scanning: {error.get('Error scanning', 'N/A')}")
                report_lines.append(f"Error: {error.get('error', 'N/A')}")
            report_lines.append("-" * 80 + "\n")
        else:
            report_lines.append("No scanning errors found.\n")

        # Save report
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_name = os.path.join(report_path, f"scan_report_{timestamp}.txt")
        with open(report_name, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))

        print(f"Report generated and saved to: {report_name}")

    def generate_report(self):
        self.generate_scan_report(self.alert, self.clear, self.error, self.report)
