import os
import hashlib
import csv
import json
from datetime import datetime

# === Configuration ===
REPORT_FOLDER = "C:\\Users\\sohai\\Desktop\\DF_REPORTS"
CSV_REPORT_PREFIX = "suspicious_file_report"
JSON_EXPORT_FILENAME = "suspicious_files_results.json"
HASH_FILE = "suspicious_hashes.txt"

# Suspicious file extensions
SUSPICIOUS_EXTENSIONS = {'.exe', '.bat', '.dll', '.vbs', '.scr', '.js'}

def load_suspicious_hashes():
    """Load suspicious hashes from a text file."""
    if os.path.exists(HASH_FILE):
        try:
            with open(HASH_FILE, "r") as f:
                return {line.strip() for line in f if line.strip()}
        except Exception as e:
            print(f"[ERROR] Failed to load suspicious hashes: {e}")
    else:
        print(f"[WARNING] Suspicious hash file not found: {HASH_FILE}")
    return set()

SUSPICIOUS_HASHES = load_suspicious_hashes()

def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"[ERROR] Could not hash file: {file_path}\nReason: {e}")
        return None

def detect_suspicious_files(directory):
    """Detect files with suspicious extensions or hashes."""
    if not os.path.isdir(directory):
        print(f"[ERROR] Directory not found: {directory}")
        return [], None

    suspicious_files = []

    print(f"[INFO] Scanning directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            # Check suspicious extension
            if ext in SUSPICIOUS_EXTENSIONS:
                suspicious_files.append({
                    "Type": "EXTENSION",
                    "File Path": file_path,
                    "Detail": ext
                })

            # Check suspicious hashes
            if SUSPICIOUS_HASHES:
                file_hash = calculate_hash(file_path)
                if file_hash and file_hash in SUSPICIOUS_HASHES:
                    suspicious_files.append({
                        "Type": "HASH",
                        "File Path": file_path,
                        "Detail": file_hash
                    })

    return suspicious_files, datetime.now().strftime("%Y%m%d_%H%M%S")

def save_to_csv(suspicious_files, timestamp):
    """Save suspicious files report to CSV."""
    os.makedirs(REPORT_FOLDER, exist_ok=True)
    csv_path = os.path.join(REPORT_FOLDER, f"{CSV_REPORT_PREFIX}_{timestamp}.csv")
    
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Type", "File Path", "Detail"])
            writer.writeheader()
            writer.writerows(suspicious_files)
        print(f"[INFO] CSV report saved: {csv_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write CSV file: {e}")

def export_to_report_generator(suspicious_files):
    """Export JSON results for report generator."""
    json_path = os.path.join(REPORT_FOLDER, JSON_EXPORT_FILENAME)
    try:
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(suspicious_files, jf, indent=4)
        print(f"[INFO] JSON exported for report generator.")
    except Exception as e:
        print(f"[ERROR] Failed to export JSON report: {e}")

def print_suspicious_files(suspicious_files):
    """Display suspicious findings in the terminal."""
    if not suspicious_files:
        print("\n[OK] No suspicious files detected.")
    else:
        print("\n[WARNING] Suspicious files detected:")
        for entry in suspicious_files:
            print(f" - [{entry['Type']}] {entry['File Path']} ({entry['Detail']})")

def main():
    dir_to_scan = input("Enter the directory to scan for suspicious files: ").strip()
    if not os.path.isdir(dir_to_scan):
        print(f"[ERROR] The directory '{dir_to_scan}' is invalid.")
        return

    suspicious_files, timestamp = detect_suspicious_files(dir_to_scan)
    print_suspicious_files(suspicious_files)

    if suspicious_files:
        save_to_csv(suspicious_files, timestamp)
        export_to_report_generator(suspicious_files)
    else:
        print("[INFO] No report generated as no suspicious files were found.")

if __name__ == "__main__":
    main()
