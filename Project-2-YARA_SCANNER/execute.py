import os
import argparse
from Script.file_scanner import FileScanner
from Script.yara_scanner import YaraScanner
from Script.ioc_automated_scanner import Exteact_ioc
from Script.Report import Report

def main(path):
    
    # Step 1: Scan files and dump file paths to JSO 
    file_scanner = FileScanner(path)
    actions = ["file" , "rules"]
    for action in actions:
        file_scanner.scan_files(action) 
        file_scanner.dump_files(action)  
    print("[+][+] end opration 1 sucess ")

    # Step 2: Scan files with YARA rules and dump results
    yara_scanner = YaraScanner()
    yara_scanner.scanner()  # Scan files using YARA rules
    yara_scanner.dump_results()  

    
    result  = Report()
    result.generate_report()
    
    
if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="File and YARA Scanner")
    parser.add_argument("-p", "--path", type=str, required=True, help="Path to scan")
    args = parser.parse_args()

    # Call main with the provided path
    main(args.path)
