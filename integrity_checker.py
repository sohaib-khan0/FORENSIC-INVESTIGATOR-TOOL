import hashlib
import os
import json
from datetime import datetime

HASH_STORAGE_FILE = "file_hashes.json"
REPORT_FOLDER = r"C:\Users\sohai\Desktop\DF_REPORTS"
LOG_FILE = os.path.join(REPORT_FOLDER, "integrity_checker_log.txt")

def create_report_dir():
    """Ensure the report directory exists."""
    os.makedirs(REPORT_FOLDER, exist_ok=True)

def log_message(message, log_entries, level="INFO"):
    """Log a message with timestamp to log file and list."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{level}] {timestamp} - {message}"
    log_entries.append(entry)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(entry + "\n")
    print(entry)

def calculate_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None
    except Exception:
        return None

def save_hashes(hashes, log_entries):
    """Save new hashes to the local storage file."""
    try:
        with open(HASH_STORAGE_FILE, "w") as f:
            json.dump(hashes, f, indent=4)
        log_message("File hashes saved successfully.", log_entries)
    except Exception as e:
        log_message(f"Failed to save file hashes: {e}", log_entries, level="ERROR")

def load_hashes(log_entries):
    """Load existing hashes from file if available."""
    if os.path.exists(HASH_STORAGE_FILE):
        try:
            with open(HASH_STORAGE_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            log_message(f"Error loading stored hashes: {e}", log_entries, level="ERROR")
            return {}
    return {}

def check_integrity(directory, log_entries):
    """Perform hash-based file integrity check in directory."""
    stored_hashes = load_hashes(log_entries)
    new_hashes = {}
    changed_files = []
    checked_files = 0

    log_message(f"Starting scan in directory: {directory}", log_entries)

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_hash(file_path)

            if file_hash:
                new_hashes[file_path] = file_hash
                checked_files += 1

                if file_path in stored_hashes and stored_hashes[file_path] != file_hash:
                    changed_files.append(file_path)

    save_hashes(new_hashes, log_entries)

    summary = f"\n[INFO] Total files scanned: {checked_files}\n"
    if changed_files:
        summary += f"\n[WARNING] Modified files detected:\n"
        for changed in changed_files:
            summary += f" - {changed}\n"
            log_message(f"File modified: {changed}", log_entries, level="WARNING")
    else:
        summary += "\n[OK] No file changes detected."
        log_message("No file modifications found.", log_entries)

    return summary

def generate_report(directory):
    """Generate report, save to file, and return content."""
    create_report_dir()
    log_entries = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"file_integrity_report_{timestamp}.txt"
    report_path = os.path.join(REPORT_FOLDER, report_filename)

    report_header = (
        f"File Integrity Checker Report\n"
        f"{'='*60}\n"
        f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Scanned Directory: {directory}\n"
        f"{'='*60}\n\n"
    )

    try:
        integrity_summary = check_integrity(directory, log_entries)
        report_content = report_header + integrity_summary + "\n\n" + "\n".join(log_entries)

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        log_message(f"Integrity report saved to {report_path}", log_entries)
        send_to_report_generator("File Integrity Checker", log_entries)

        return report_content
    except Exception as e:
        log_message(f"Failed to generate integrity report: {e}", log_entries, level="ERROR")
        return "[ERROR] Failed to complete the integrity check."

def send_to_report_generator(module_name, log_entries):
    """Send analysis logs to final report generator."""
    try:
        from report_generator import add_to_final_report
        add_to_final_report(module_name, log_entries)
    except ImportError:
        print("[WARNING] report_generator.py not found. Skipping report integration.")

if __name__ == "__main__":
    dir_to_scan = input("Enter the directory to scan for integrity check: ").strip()
    if not os.path.isdir(dir_to_scan):
        print(f"[ERROR] The directory '{dir_to_scan}' does not exist.")
    else:
        final_report = generate_report(dir_to_scan)
        print(final_report)
