# Technical Electives Course Map

A comprehensive command-line tool for analyzing technical elective courses, checking prerequisites, and planning your academic path. This tool parses PDF course catalogs and helps you find eligible courses based on your completed coursework.

## Features

- 📚 **Course Parsing**: Extract and organize course data from PDF catalogs
- 🔍 **Smart Search**: Find courses by keyword, major, or academic level
- ✅ **Prerequisite Checking**: Automatically determine which courses you're eligible for
- 📊 **Statistics**: Get comprehensive statistics about available courses
- 💾 **CSV Export**: Export filtered results for further analysis
- 🎨 **Colored Output**: Easy-to-read terminal output with color coding
- 🎓 **Academic Level Filtering**: Separate undergraduate and graduate courses

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Virtual environment (recommended)

### Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install required dependencies:
   ```bash
   pip install PyMuPDF
   ```

### Usage

The easiest way to use the tool is with the provided shell script:

```bash
# Show help
./tech_elect_map --help

# Basic usage - show all courses
./tech_elect_map courses.pdf

# Filter by major and academic level
./tech_elect_map courses.pdf --major CpE --undergrad

# Search for specific topics
./tech_elect_map courses.pdf --search "machine learning" --verbose

# Check eligible courses based on completed coursework
./tech_elect_map courses.pdf --completed-file my_courses.txt --eligible

# Generate statistics and export to CSV
./tech_elect_map courses.pdf --stats --output results.csv
```

Alternatively, you can use the Python script directly:
```bash
.venv/bin/python tech_elect_cli.py courses.pdf [options]
```

## Command Line Options

```
positional arguments:
  pdf_file              Path to the technical electives PDF file

options:
  -h, --help            Show help message and exit
  -u, --undergrad       Show only undergraduate courses
  -g, --graduate        Show only graduate courses
  -m, --major {EE,CpE,CS,IT,EE2,CpE1,EE3}
                        Filter by major
  --search SEARCH       Search courses by keyword
  --completed-file COMPLETED_FILE
                        File containing completed courses
  --eligible            Show only eligible courses (requires --completed-file)
  -v, --verbose         Show detailed course information
  -s, --stats           Show course statistics
  --output OUTPUT       Export results to CSV file
```

## Completed Courses File Format

Create a text file listing your completed courses, one per line or comma-separated:

**Format 1 (one per line):**
```
EEL 3123C
EEL 3801C
EEE 3342C
COP 3503C
```

**Format 2 (comma-separated):**
```
EEL 3123C, EEL 3801C, EEE 3342C, COP 3503C, EGN 3211
```

## Examples

### Find Machine Learning Courses
```bash
./tech_elect_map courses.pdf --search "machine learning" --verbose
```

### Check Eligible CpE Undergraduate Courses
```bash
./tech_elect_map courses.pdf --completed-file my_courses.txt --eligible --major CpE --undergrad
```

### Generate Complete Course Statistics
```bash
./tech_elect_map courses.pdf --stats --output course_analysis.csv
```

### Search for VLSI-related Courses
```bash
./tech_elect_map courses.pdf --search "VLSI" --verbose
```

## Output Features

- **Color-coded status**: ✅ Success, ❌ Error, ⚠️ Warning
- **Formatted tables**: Clean, aligned course information
- **Prerequisite parsing**: Automatically extracts and displays prerequisites
- **Eligibility checking**: Shows which courses you can take based on completed work
- **CSV export**: Export filtered results for spreadsheet analysis

## Web Visualization

This project also includes a web-based visualization tool. To use it:

1. Install Flask: `pip install flask flask-cors`
2. Run the web server: `python run_visualization.py`
3. Open your browser to `http://localhost:5001`

The web interface provides:
- Interactive course dependency graphs
- Multiple visualization modes
- Real-time filtering and search
- Modern, responsive design

## Project Structure

```
tech-elect/
├── tech_elect_map.py          # Core course parsing and analysis logic
├── tech_elect_cli.py          # Command-line interface
├── tech_elect_map             # Shell script wrapper
├── course_api.py              # Flask web API
├── static/index.html          # Web visualization interface
├── run_visualization.py       # Web server runner
├── sample_courses.txt         # Example completed courses file
└── README.md                  # This file
```

## Supported Majors

- **EE**: Electrical Engineering
- **CpE**: Computer Engineering  
- **CS**: Computer Science
- **IT**: Information Technology
- **EE2, EE3**: Specialized EE tracks
- **CpE1**: Specialized CpE track

## Troubleshooting

### Virtual Environment Issues
If you get "ModuleNotFoundError: No module named 'pymupdf'":
```bash
source .venv/bin/activate
pip install PyMuPDF
```

### Permission Issues
If the shell script isn't executable:
```bash
chmod +x tech_elect_map
```

### PDF Parsing Issues
Ensure your PDF file is readable and contains structured course information. The tool expects course codes in formats like "EEL 3123C" or "CAP 4630".

## Contributing

This tool was developed to help students navigate technical elective requirements. Feel free to:
- Report bugs or issues
- Suggest new features
- Contribute improvements
- Share with other students

## License

This project is released for educational use. Please respect your institution's academic policies when using this tool.

---

**Happy Course Planning! 🎓**