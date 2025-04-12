import os
import shutil
from datetime import datetime

REPORT_DIR = r"C:\Users\sohai\Desktop\DF_REPORTS"
LOG_FILE = os.path.join(REPORT_DIR, "collection_log.txt")

def create_report_directory():
    """Ensure the DF_REPORTS directory exists."""
    os.makedirs(REPORT_DIR, exist_ok=True)

def save_analysis_to_report(report_data, report_filename):
    """Save the analysis report to a text file in REPORT_DIR."""
    try:
        report_file_path = os.path.join(REPORT_DIR, report_filename)
        with open(report_file_path, 'a', encoding='utf-8') as report_file:
            report_file.write(report_data + "\n\n")
        print(f"[INFO] Report saved to: {report_file_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save report: {e}")

def generate_report(source_dir, destination_dir, collected_count, timestamp, log_entries):
    """Generate and save a detailed artifact collection report."""
    report_data = f"Artifact Collection Report - {timestamp}\n"
    report_data += "=" * 60 + "\n"
    report_data += f"Source Directory: {source_dir}\n"
    report_data += f"Destination Directory: {destination_dir}\n\n"
    report_data += "\n".join(log_entries)
    report_data += f"\n\nTotal Files Collected: {collected_count}\n"
    report_data += f"Collection Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report_data += "=" * 60

    report_filename = f"artifact_collection_report_{timestamp}.txt"
    save_analysis_to_report(report_data, report_filename)

    # ✅ Return summary for report_generator.py
    return report_data

def collect_artifacts(source_dir, destination_dir):
    """Collect forensic artifacts with logging and reporting."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_dir = os.path.join(destination_dir, f"artifacts_{timestamp}")
    os.makedirs(artifact_dir, exist_ok=True)

    collected_count = 0
    log_entries = []

    create_report_directory()

    try:
        with open(LOG_FILE, "a", encoding='utf-8') as log_file:
            log_file.write(f"\n[LOG] Artifact Collection - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            for root, _, files in os.walk(source_dir):
                for file in files:
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(artifact_dir, file)

                    # Handle duplicate filenames
                    if os.path.exists(destination_path):
                        base, ext = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(destination_path):
                            new_file = f"{base}_{counter}{ext}"
                            destination_path = os.path.join(artifact_dir, new_file)
                            counter += 1

                    try:
                        shutil.copy2(source_path, destination_path)
                        collected_count += 1
                        msg = f"[INFO] Collected: {destination_path}"
                        log_file.write(msg + "\n")
                        log_entries.append(msg)
                    except Exception as e:
                        error_msg = f"[ERROR] Failed to collect {file}: {e}"
                        log_file.write(error_msg + "\n")
                        log_entries.append(error_msg)

        report_data = generate_report(source_dir, artifact_dir, collected_count, timestamp, log_entries)

        print(f"\n✅ Artifact collection completed successfully!")
        print(f"   → {collected_count} files saved to: {artifact_dir}")
        print(f"   → Log file updated at: {LOG_FILE}")
        return report_data  # ✅ For report_generator

    except Exception as e:
        print(f"[ERROR] Unexpected error during artifact collection: {e}")
        return "[ERROR] Artifact collection failed."

# For direct CLI usage
if __name__ == "__main__":
    print("=== Automated Artifact Collection ===")
    source = input("Enter the source directory to collect from: ").strip()
    destination = input("Enter the destination directory to save artifacts: ").strip()

    if not os.path.isdir(source):
        print(f"[ERROR] The source directory does not exist: {source}")
    elif not os.path.isdir(destination):
        print(f"[ERROR] The destination directory does not exist: {destination}")
    else:
        collect_artifacts(source, destination)
