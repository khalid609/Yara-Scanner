import yara
import json
import os
import time
from Script.json_organizer import JsonOrganizer
from Script.ioc_automated_scanner import Exteact_ioc

class YaraScanner:
    def __init__(self):
        obj = JsonOrganizer()
        self._feed = obj.load_yara_feed_data()  # Ensure this returns a list of dicts with "file path"
        self._ioc_obj = Exteact_ioc()  # Object for IOC.py

        # Lists
        self.alert = []
        self.error = []
        self.notfound = []

        # Paths
        self.result_ALERT = obj.get_alert_results_json_path()
        self.result_ERROR = obj.get_error_results_json_path()
        self.result_NOTFOUND = obj.get_not_found_results_json_path()

        # YARA rules path
        self.yara_path = obj.get_yara_rules_json_path()

    def scanner(self):
        # Load YARA rule file paths from JSON
        with open(self.yara_path, "r") as f:
            rules_path = json.load(f)  # Expects a list of rule file paths

        alerts_dict = {}  # Dictionary to store alerts, keyed by file path

        for rule_file in rules_path:
            try:
                # Compile YARA rules for the current rule file
                rules = yara.compile(filepath=rule_file["file path"])
                print(f"Loaded rule: {rule_file['file path']}")
            except yara.Error as e:
                print(f"YARA compilation error for {rule_file['file path']}: {e}")
                continue  # Skip to the next rule file
            except FileNotFoundError:
                print(f"YARA rule file not found: {rule_file['file path']}")
                continue  # Skip to the next rule file

            for feed in self._feed:
                file_path = feed.get("file path")
                if not file_path:
                    print(f"Invalid feed entry: {feed}")
                    continue

                try:
                    matches = rules.match(file_path)

                    if matches:
                        # Calculate hash only once per file
                        hash_value = self._ioc_obj.Get_Hash(file_path)

                        if file_path not in alerts_dict:
                            file_stats = os.stat(file_path)

                            # Full metadata as a dictionary
                            metadata = {
                                "size_bytes": file_stats.st_size,
                                "created_time": time.ctime(file_stats.st_ctime),
                                "modified_time": time.ctime(file_stats.st_mtime),
                                "accessed_time": time.ctime(file_stats.st_atime),
                                "mode": file_stats.st_mode,
                                "uid": file_stats.st_uid,
                                "gid": file_stats.st_gid,
                                "inode": file_stats.st_ino,
                                "device": file_stats.st_dev,
                                "nlink": file_stats.st_nlink,
                            }

                            alerts_dict[file_path] = {
                                "[ALERT]": "Malware detected",
                                "matches found": file_path,
                                "hash": hash_value,
                                "Rules": [],
                                "metadata": metadata
                            }

                        # Append matching rules to the file's entry
                        for match in matches:
                            if match.rule not in alerts_dict[file_path]["Rules"]:
                                alerts_dict[file_path]["Rules"].append(match.rule)

                    else:
                        if file_path not in alerts_dict and file_path not in [nf["No matches found"] for nf in self.notfound]:
                            self.notfound.append({"No matches found": file_path})

                except Exception as e:
                    if file_path not in [err["Error scanning"] for err in self.error]:
                        self.error.append({"Error scanning": file_path, "error": str(e)})

        # Convert the alerts dictionary to a list
        if alerts_dict:
            self.alert = list(alerts_dict.values())

        # Print the number of files with matches
        if self.alert:
            print(f"Found {len(alerts_dict)} files with matches.")

    def dump_results(self):
        # Always dump results, even if lists are empty
        with open(self.result_ALERT, "w", encoding="utf-8") as f:
            json.dump(self.alert, f, indent=4)
        print(f"(Alerts) dumped to {self.result_ALERT}")

        with open(self.result_ERROR, "w", encoding="utf-8") as f:
            json.dump(self.error, f, indent=4)
        print(f"(Errors) dumped to {self.result_ERROR}")

        with open(self.result_NOTFOUND, "w", encoding="utf-8") as f:
            json.dump(self.notfound, f, indent=4)
        print(f"(Not found) results dumped to {self.result_NOTFOUND}")
