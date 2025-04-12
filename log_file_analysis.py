import os
import re
import time

# Define suspicious patterns (you can customize this list)
SUSPICIOUS_PATTERNS = [
    r"failed login",
    r"unauthorized access",
    r"brute force",
    r"malware",
    r"suspicious activity",
    r"error 403",
    r"error 404"
]

REPORT_DIR = "C:/Users/sohai/Desktop/DF_REPORTS"

def analyze_log_file(log_file_path):
    """Analyze a single log file for suspicious activity and return results."""
    results = []
    
    if not os.path.exists(log_file_path):
        return [f"[ERROR] Log file not found: {log_file_path}"]

    if not os.access(log_file_path, os.R_OK):
        return [f"[ERROR] Permission denied: {log_file_path}. Please check the file permissions."]

    try:
        with open(log_file_path, 'r', encoding="utf-8", errors="ignore") as log_file:
            logs = log_file.readlines()

        for line in logs:
            for pattern in SUSPICIOUS_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    results.append(line.strip())

        # Prepare the report
        os.makedirs(REPORT_DIR, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(REPORT_DIR, f"log_analysis_{timestamp}.txt")

        with open(report_file, 'w', encoding="utf-8") as f:
            f.write(f"Log File Analysis Report\nAnalyzed File: {log_file_path}\n\n")
            if results:
                f.write("Suspicious Entries Found:\n")
                for entry in results:
                    f.write(f"- {entry}\n")
            else:
                f.write("No suspicious activity detected.\n")

        print(f"[INFO] Log analysis saved to: {report_file}")
        return results if results else ["No suspicious activity detected."]

    except PermissionError:
        return [f"[ERROR] Permission denied while opening the file: {log_file_path}"]
    except Exception as e:
        return [f"[ERROR] Failed to analyze log file: {e}"]

def analyze_logs_in_directory(directory_path):
    """Analyze all .log or .txt files in a directory recursively."""
    final_results = []
    if not os.path.isdir(directory_path):
        return [f"[ERROR] Provided path is not a directory: {directory_path}"]

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.log') or file.endswith('.txt'):
                log_file_path = os.path.join(root, file)
                result = analyze_log_file(log_file_path)
                final_results.extend(result)

    return final_results

# Optional direct script usage
if __name__ == "__main__":
    path = input("Enter the path to the log file or directory: ").strip()
    if os.path.isdir(path):
        results = analyze_logs_in_directory(path)
    else:
        results = analyze_log_file(path)
    
    print("\n".join(results))
