import os
import pytsk3
from datetime import datetime



REPORT_FOLDER = r"C:\Users\sohai\Desktop\DF_REPORTS"
RECOVERY_FOLDER = os.path.join(REPORT_FOLDER, "recovered_files")
LOG_FILE = os.path.join(REPORT_FOLDER, "disk_recovery_log.txt")

def create_directories():
    """Ensure report and recovery directories exist."""
    os.makedirs(REPORT_FOLDER, exist_ok=True)
    os.makedirs(RECOVERY_FOLDER, exist_ok=True)

def log_message(message, log_entries, level="INFO"):
    """Log a message to both list and file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{level}] {timestamp} - {message}"
    log_entries.append(entry)
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(entry + "\n")
    print(entry)

def recover_file(file_entry, file_name, log_entries):
    """Recover a single deleted file."""
    try:
        recovered_path = os.path.join(RECOVERY_FOLDER, file_name)

        # Handle duplicates
        base, ext = os.path.splitext(file_name)
        counter = 1
        while os.path.exists(recovered_path):
            recovered_path = os.path.join(RECOVERY_FOLDER, f"{base}_{counter}{ext}")
            counter += 1

        # Write recovered file
        with open(recovered_path, 'wb') as recovered_file:
            file_data = file_entry.read_random(0, file_entry.info.meta.size)
            recovered_file.write(file_data)

        log_message(f"Recovered: {recovered_path}", log_entries)
        return recovered_path
    except Exception as e:
        log_message(f"Failed to recover {file_name}: {e}", log_entries, level="ERROR")
        return None

def analyze_disk_image(image_path):
    """Main function to analyze disk image and recover deleted files."""
    create_directories()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_entries = []
    recovered_count = 0
    recovered_files = []

    try:
        img_info = pytsk3.Img_Info(image_path)
        fs = pytsk3.FS_Info(img_info)
        root_dir = fs.open_dir("/")

        for entry in root_dir:
            try:
                if entry.info.meta and entry.info.meta.flags == pytsk3.TSK_FS_META_FLAG_UNALLOC:
                    file_name = entry.info.name.name.decode("utf-8", errors="ignore")
                    path = recover_file(entry, file_name, log_entries)
                    if path:
                        recovered_count += 1
                        recovered_files.append(path)
            except Exception as e:
                log_message(f"Error processing file entry: {e}", log_entries, level="ERROR")

        write_report(image_path, recovered_count, recovered_files, timestamp, log_entries)
        send_to_report_generator("Disk Image Analysis", log_entries)
    except Exception as e:
        log_message(f"Failed to analyze disk image: {e}", log_entries, level="ERROR")

def write_report(image_path, count, recovered_files, timestamp, log_entries):
    """Write a full analysis report to file."""
    report_filename = f"disk_image_recovery_report_{timestamp}.txt"
    report_path = os.path.join(REPORT_FOLDER, report_filename)

    with open(report_path, 'w', encoding='utf-8') as report:
        report.write(f"Disk Image Recovery Report\n")
        report.write("="*60 + "\n")
        report.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write(f"Analyzed Image: {image_path}\n")
        report.write(f"Recovered Files: {count}\n")
        report.write(f"Recovery Path: {RECOVERY_FOLDER}\n")
        report.write("="*60 + "\n\n")
        for log in log_entries:
            report.write(log + "\n")

    log_message(f"Report saved to: {report_path}", log_entries)

def send_to_report_generator(module_name, log_entries):
    """Send results to the report generator."""
    try:
        from report_generator import add_to_final_report
        add_to_final_report(module_name, log_entries)
    except ImportError:
        print("[WARNING] report_generator.py not found. Skipping report integration.")

if __name__ == "__main__":
    image_path = input("Enter the full path to the disk image: ").strip()
    if not os.path.exists(image_path):
        print(f"[ERROR] The disk image {image_path} does not exist.")
    else:
        analyze_disk_image(image_path)
