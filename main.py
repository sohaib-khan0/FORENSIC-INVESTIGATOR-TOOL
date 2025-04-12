import tkinter as tk
from tkinter import filedialog, messagebox
import os
import time
from metadata_analysis import analyze_metadata
from timeline_generator import generate_timeline
from suspicious_file_detection import detect_suspicious_files
from disk_image_analysis import analyze_disk_image
from log_file_analysis import analyze_log_file
from automated_artifact_collection import collect_artifacts
from report_generator import generate_report
from integrity_checker import generate_report as generate_integrity_report

REPORTS_DIR = "C:/Users/sohai/Desktop/DF_REPORTS"
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

results = {}  # Global dictionary to accumulate results

# GUI functionality
class ForensicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Forensic Investigator Tool")
        self.configure(bg="#f0f0f0")
        self.geometry("600x600")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Enter the directory path or file:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        self.entry_path = tk.Entry(self, width=60)
        self.entry_path.pack(pady=5)

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Select File", command=self.open_file_dialog).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Select Directory", command=self.open_directory_dialog).grid(row=0, column=1, padx=5)

        self.add_button("File Integrity Checker", lambda: self.run_analysis("File Integrity", generate_integrity_report))
        self.add_button("Digital Evidence Timeline", lambda: self.run_analysis("Digital Evidence Timeline", generate_timeline))
        self.add_button("Suspicious File Detection", lambda: self.run_analysis("Suspicious File Detection", detect_suspicious_files))
        self.add_button("Forensic Disk Image Analysis", lambda: self.run_analysis("Forensic Disk Image Analysis", analyze_disk_image))
        self.add_button("Metadata Analysis", lambda: self.run_analysis("Metadata Analysis", analyze_metadata))
        self.add_button("Log File Analysis", lambda: self.run_analysis("Log File Analysis", analyze_log_file))
        self.add_button("Automated Artifact Collection", lambda: self.run_artifact_collection())
        self.add_button("Generate Full Report", self.generate_full_report)

    def add_button(self, text, command):
        tk.Button(self, text=text, command=command, width=40, bg="#007acc", fg="white",
                  font=("Arial", 10, "bold")).pack(pady=4)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
        if file_path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, file_path)

    def open_directory_dialog(self):
        dir_path = filedialog.askdirectory(title="Select a directory")
        if dir_path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, dir_path)

    def run_analysis(self, label, analysis_function):
        try:
            path = self.entry_path.get()
            if not path:
                messagebox.showerror("Input Error", "Please enter a valid path.")
                return

            result = analysis_function(path)
            results[label] = result if isinstance(result, list) else [str(result)]

            # Save results to individual text file
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(REPORTS_DIR, f"{label.replace(' ', '_')}_{timestamp}.txt")
            with open(output_path, 'w') as f:
                f.write("\n".join(results[label]))

            messagebox.showinfo(label, f"Analysis completed. Results saved at:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def run_artifact_collection(self):
        try:
            source = self.entry_path.get()
            if not source:
                messagebox.showerror("Input Error", "Please enter a valid source path.")
                return
            result = collect_artifacts(source, REPORTS_DIR)
            results['Automated Artifact Collection'] = result if isinstance(result, list) else [str(result)]
            messagebox.showinfo("Automated Artifact Collection", "Artifacts collected successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def generate_full_report(self):
        try:
            report_filename = f"forensic_report_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
            report_path = os.path.join(REPORTS_DIR, report_filename)
            generate_report(results, report_path)
            messagebox.showinfo("Report Generated", f"PDF Report saved at:\n{report_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

if __name__ == "__main__":
    app = ForensicApp()
    app.mainloop()
