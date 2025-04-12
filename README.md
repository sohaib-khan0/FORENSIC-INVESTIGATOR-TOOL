# FORENSIC-INVESTIGATOR-TOOL


---

```markdown
# Forensic Investigator Tool

This is a forensic investigation tool that I've developed to help with digital forensics tasks like file integrity checking, suspicious file detection, log file analysis, and disk image analysis. The tool is designed to be modular, so each feature can be used independently or as part of a larger forensic investigation workflow. It supports both command-line and graphical user interfaces (CLI and GUI) and generates detailed forensic reports.

## Features

- **File Integrity Checker**:  
  This module checks files in a specified directory for integrity by comparing their hash values against a known database of hashes. It helps identify any unauthorized modifications to files.

- **Digital Evidence Timeline Generator**:  
  It extracts timestamps from files and generates a timeline based on their activity, helping investigators track when certain files were created, modified, or accessed.

- **Suspicious File Detection**:  
  This module identifies suspicious files by checking for unusual file types, extensions, or patterns that could indicate malicious files or files of interest for further investigation.

- **Forensic Disk Image Analysis**:  
  I’ve integrated `pytsk3` for analyzing disk images. It allows me to recover deleted files and gather detailed metadata from disk images like `.img` files.

- **Log File Analysis**:  
  This module scans log files (e.g., `.log`, `.txt`) for suspicious activity like failed login attempts, unauthorized access, or error codes.

- **Automated Artifact Collection**:  
  It collects forensic artifacts such as browsing history, recently accessed files, and other potential indicators of compromise from the system.

- **Report Generation**:  
  The tool generates detailed forensic reports in PDF format, summarizing the findings from the various analysis modules. It uses the `ReportLab` library for customizable PDF generation.

## Technologies Used

- **Python 3**: The main programming language for the project.
- **Tkinter**: Used for creating the GUI.
- **pytsk3**: For disk image analysis.
- **python-magic**: For identifying file types.
- **hashlib**: For file integrity checking.
- **pandas**: For managing and organizing analysis results.
- **ReportLab**: For generating detailed forensic reports in PDF format.

## How to Use

### Running the Tool via CLI

1. Clone this repository to your local machine:

   ```
   git clone https://github.com/yourusername/forensic-investigator-tool.git
   cd forensic-investigator-tool
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the tool via CLI by executing:

   ```
   python main.py
   ```

### Running the Tool via GUI

1. Ensure all dependencies are installed as shown above.
2. Run the tool using the command:

   ```
   python main.py --gui
   ```

   This will open the graphical user interface where you can select files or directories to analyze and choose the features to run.

## Testing

I have written both unit and integration tests for each module to ensure that they work as expected. You can run the tests using:

```
python -m unittest discover tests/
```

## Contribution

If you want to contribute to this project, feel free to fork the repository and create a pull request. Please ensure to write tests for any new features and follow the existing coding style.

## License

This project is licensed under the MIT License.

---

Feel free to customize this `README.md` file as needed. It reflects the details of your project and its features and provides clear instructions for usage and contribution.
```
