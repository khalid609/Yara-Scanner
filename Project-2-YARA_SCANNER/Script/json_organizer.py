import os
import json
from datetime import datetime

class JsonOrganizer:

    def __init__(self):
        root_dir = os.path.dirname(__file__)

        self.directory_content_json_path = os.path.join(root_dir, "../json/directory_content.json")

        self.yara_rules_directory_path = os.path.join(root_dir, "../yara/rules") 
        
        self.rule_file = os.path.join(root_dir, "../yara", "rules.json")
        self.yara_rules_json_path = os.path.join(root_dir, "../yara/rules.json")

        
        
        self.alert_results_json_path = os.path.join(root_dir, "../json/alert_results.json")
        self.error_results_json_path = os.path.join(root_dir, "../json/error_results.json")
        self.not_found_results_json_path = os.path.join(root_dir, "../json/not_found_results.json")
        
 

        # Path for report
        self.report_txt_path = os.path.join(root_dir, "../Report/")

        # List to store YARA feed data
        self.yara_feed_data = []




    def get_directory_content_json_path(self):
        return self.directory_content_json_path

    # Return path for rules JSON file
    def get_yara_rules_json_path(self):
        return self.yara_rules_json_path

    # Return path for YARA rules directory
    def get_yara_rules_directory_path(self):
        return self.yara_rules_directory_path

    # Getters for scanner
    def get_alert_results_json_path(self):
        """Return the path for ALERT results JSON file."""
        return self.alert_results_json_path

    def get_error_results_json_path(self):
        """Return the path for ERROR results JSON file."""
        return self.error_results_json_path

    def get_not_found_results_json_path(self):
        """Return the path for NOTFOUND results JSON file."""
        return self.not_found_results_json_path

    def get_report_pdf_path(self):
        """Return the path for the report PDF file."""
        
        return self.report_pdf_path
    def get_report_txt_path(self):
        """Return the path for the report PDF file."""
        return self.report_txt_path
    def load_yara_feed_data(self):
        """
        Load directory content JSON file and return data for YARA scanner.
        Returns:
            list: List of file paths to be scanned by YARA.
        """
        with open(self.directory_content_json_path, "r") as file:
            data = json.load(file)

        self.yara_feed_data = data
        
        return self.yara_feed_data
