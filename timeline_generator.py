import os
import csv
import json
from datetime import datetime

# === Configuration ===
REPORT_FOLDER = "C:\\Users\\sohai\\Desktop\\DF_REPORTS"
CSV_REPORT_PREFIX = "digital_timeline_report"
JSON_EXPORT_FILENAME = "timeline_results.json"

def generate_timeline(directory, sort_by="modified"):
    """Generate a digital evidence timeline from file metadata."""
    if not os.path.isdir(directory):
        print(f"[ERROR] Directory not found: {directory}")
        return [], None

    timeline = []

    print(f"[INFO] Scanning directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                stats = os.stat(file_path)
                created = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                modified = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                accessed = datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')

                timeline.append({
                    "File": file_path,
                    "Created": created,
                    "Modified": modified,
                    "Accessed": accessed
                })

            except Exception as e:
                print(f"[ERROR] Failed to process file: {file_path}\nReason: {e}")

    if not timeline:
        print("[INFO] No files found to generate a timeline.")
        return [], None

    # Sorting
    sort_key = sort_by.capitalize()
    if sort_key not in ["Created", "Modified", "Accessed"]:
        sort_key = "Modified"
    timeline.sort(key=lambda x: x[sort_key])

    return timeline, sort_key


def save_to_csv(results, sort_by):
    """Save timeline results to a CSV file."""
    os.makedirs(REPORT_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file_path = os.path.join(REPORT_FOLDER, f"{CSV_REPORT_PREFIX}_{timestamp}.csv")

    try:
        with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["File", "Created", "Modified", "Accessed"])
            writer.writeheader()
            writer.writerows(results)
        print(f"[INFO] CSV timeline saved: {csv_file_path}")
    except Exception as e:
        print(f"[ERROR] Could not save CSV report: {e}")


def export_to_report_generator(results):
    """Export results to JSON for report generator."""
    json_path = os.path.join(REPORT_FOLDER, JSON_EXPORT_FILENAME)
    try:
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(results, jf, indent=4)
        print(f"[INFO] JSON exported for report generator.")
    except Exception as e:
        print(f"[ERROR] Failed to export timeline to JSON: {e}")


def print_timeline(results):
    """Print a human-readable timeline to the terminal."""
    print("\nDigital Evidence Timeline:\n" + "-" * 50)
    for event in results:
        print(f"File     : {event['File']}")
        print(f"Created  : {event['Created']}")
        print(f"Modified : {event['Modified']}")
        print(f"Accessed : {event['Accessed']}")
        print("-" * 50)


def main():
    dir_to_scan = input("Enter the directory to generate the timeline: ").strip()
    if not os.path.isdir(dir_to_scan):
        print(f"[ERROR] The directory '{dir_to_scan}' does not exist or is not valid.")
        return

    sort_by = input("Sort by (created, modified, accessed): ").strip().lower() or "modified"
    results, sort_used = generate_timeline(dir_to_scan, sort_by)

    if results:
        print_timeline(results)
        save_to_csv(results, sort_used)
        export_to_report_generator(results)
    else:
        print("[INFO] No timeline data to save.")


if __name__ == "__main__":
    main()
