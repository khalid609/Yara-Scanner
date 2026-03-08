import os
import json
# from Script.json_organizer import JsonOrganizer
from Script.json_organizer import JsonOrganizer

class FileScanner:

    def __init__(self, path):
        self.path = path
        self.dir_content = []
        self.rule_content = []
        self.VT__content = []

        self._org = JsonOrganizer()
        

    def scan_files(self ,action):
        if action == "file":
            print("[+] Scan files start")

            scan_path = self.path
            target = self.dir_content

        elif action == "rules":
            print("[+] Scan rules start")

            scan_path = self._org.get_yara_rules_directory_path()
            target = self.rule_content
        

        for root, _, files in os.walk(scan_path):
            for file in files:
                path = os.path.join(root, file)
                target.append({"file path": path})

    
    def dump_files(self, dump_location):
        if dump_location == "file":
            print("[+] Dumping files start")

            dump_path = self._org.get_directory_content_json_path()
            data = self.dir_content

        elif dump_location == "rules":
            print("[+] Dumping rules start")
            
            dump_path = self._org.get_yara_rules_json_path()
            data = self.rule_content

        else:
            raise ValueError("Dump location must be 'file' or 'rules'")

        with open(dump_path, "w") as f:
            json.dump(data, f, indent=2)
 
    def get_VT(self):
        return self.VT__content