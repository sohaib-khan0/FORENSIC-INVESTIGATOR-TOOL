import magic
import os
import time
from datetime import datetime
import json

# Configuration
REPORT_FOLDER = "C:\\Users\\sohai\\Desktop\\DF_REPORTS"
REPORT_PREFIX = "metadata_analysis_report"
ANALYSIS_TYPE = "Metadata Analysis"

def get_file_metadata(file_path):
    """Extract metadata for a given file."""
    metadata = {"File": file_path}
    try:
        metadata["Size (bytes)"] = os.path.getsize(file_path)
        metadata["MIME Type"] = magic.Magic(mime=True).from_file(file_path)
        metadata["Created"] = time.ctime(os.path.getctime(file_path))
        metadata["Modified"] = time.ctime(os.path.getmtime(file_path))
        metadata["Accessed"] = time.ctime(os.path.getatime(file_path))
    except FileNotFoundError:
        metadata["Error"] = "File not found"
    except PermissionError:
        metadata["Error"] = "Permission denied"
    except Exception as e:
        metadata["Error"] = f"Unexpected error: {e}"
    return metadata

def write_metadata_to_txt(report_path, metadata_list):
    """Write metadata to a human-readable report."""
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"{ANALYSIS_TYPE} Report\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for data in metadata_list:
                f.write("[FILE METADATA]\n")
                for key, value in data.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")
    except Exception as e:
        print(f"[ERROR] Failed to write TXT report: {e}")

def send_to_report_generator(results):
    """Send metadata results to the final PDF report generator."""
    try:
        json_path = os.path.join(REPORT_FOLDER, "metadata_results.json")
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(results, jf, indent=4)
        print("[INFO] Metadata results sent to report_generator.py")
    except Exception as e:
        print(f"[ERROR] Failed to export JSON for report generator: {e}")

def analyze_metadata(directory):
    """Main function to perform metadata analysis."""
    if not os.path.isdir(directory):
        print(f"[ERROR] Invalid directory: {directory}")
        return

    print(f"[INFO] Scanning directory: {directory}")
    os.makedirs(REPORT_FOLDER, exist_ok=True)

    metadata_results = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            result = get_file_metadata(file_path)
            metadata_results.append(result)

    # Save TXT Report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_report_path = os.path.join(REPORT_FOLDER, f"{REPORT_PREFIX}_{timestamp}.txt")
    write_metadata_to_txt(txt_report_path, metadata_results)

    # Send to report_generator
    send_to_report_generator(metadata_results)

    print(f"[INFO] Report saved to {txt_report_path}")
    return metadata_results

if __name__ == "__main__":
    user_input = input("Enter directory for metadata analysis: ").strip()
    if os.path.isdir(user_input):
        analyze_metadata(user_input)
    else:
        print(f"[ERROR] The directory '{user_input}' does not exist.")
