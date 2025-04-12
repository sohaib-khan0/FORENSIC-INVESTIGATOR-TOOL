import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# === Configuration ===
REPORT_FOLDER = "C:\\Users\\sohai\\Desktop\\DF_REPORTS"
FINAL_REPORT_NAME = "final_forensic_report.pdf"

# Define the expected JSON outputs from each module
ANALYSIS_MODULES = {
    "File Integrity Checker": "file_integrity_results.json",
    "Digital Evidence Timeline": "evidence_timeline_results.json",
    "Suspicious File Detection": "suspicious_files_results.json",
    "Metadata Analysis": "metadata_analysis_results.json",
    "Log File Analysis": "log_analysis_results.json",
    "Disk Image Analysis": "disk_image_results.json",
    "Artifact Collection": "artifact_results.json"
}

def load_analysis_results():
    """Load JSON result files from all analysis modules."""
    combined_results = {}
    for section, filename in ANALYSIS_MODULES.items():
        file_path = os.path.join(REPORT_FOLDER, filename)
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Convert to flat string list if needed
                    if isinstance(data, list):
                        combined_results[section] = [
                            f"{entry['Type']}: {entry['File Path']} ({entry['Detail']})" if isinstance(entry, dict)
                            else str(entry) for entry in data
                        ]
                    else:
                        combined_results[section] = [str(data)]
            else:
                combined_results[section] = ["[INFO] No data found."]
        except Exception as e:
            combined_results[section] = [f"[ERROR] Failed to read {filename}: {e}"]
    return combined_results

def generate_report(results, report_path):
    """Generate a well-formatted PDF report summarizing forensic results."""
    try:
        c = canvas.Canvas(report_path, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)

        # Title and timestamp
        c.drawString(50, height - 50, "Digital Forensics Investigator Report")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Summary Section
        y_position = height - 110
        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y_position, "Summary")
        y_position -= 20
        c.setFont("Helvetica", 11)

        toc_items = []
        for section, lines in results.items():
            summary = f"{section}: {len(lines)} item(s)"
            c.drawString(50, y_position, summary)
            toc_items.append((section, y_position))
            y_position -= 15

        # Space before details
        y_position -= 20

        # Detailed Analysis Sections
        for section, lines in results.items():
            if y_position < 100:
                c.showPage()
                y_position = height - 50

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_position, section)
            y_position -= 20
            c.setFont("Helvetica", 11)

            for line in lines:
                wrapped = simpleSplit(line, "Helvetica", 11, width - 100)
                for wrap in wrapped:
                    if y_position < 50:
                        c.showPage()
                        c.setFont("Helvetica", 11)
                        y_position = height - 50
                    c.drawString(50, y_position, wrap)
                    y_position -= 15

            y_position -= 20  # Space between sections

        # Table of Contents (on new page)
        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, "Table of Contents")
        toc_y = height - 80
        c.setFont("Helvetica", 11)

        for section, pos in toc_items:
            c.drawString(50, toc_y, f"{section} - Page 1")
            toc_y -= 15

        # Footer with page number
        c.setFont("Helvetica", 10)
        c.drawString(width - 60, 20, f"Page {c.getPageNumber()}")

        # Save the final PDF
        c.save()
        print(f"[INFO] PDF report saved: {report_path}")
    except Exception as e:
        print(f"[ERROR] Failed to generate report: {e}")

def main():
    os.makedirs(REPORT_FOLDER, exist_ok=True)
    output_path = os.path.join(REPORT_FOLDER, FINAL_REPORT_NAME)
    results = load_analysis_results()
    generate_report(results, output_path)

if __name__ == "__main__":
    main()
