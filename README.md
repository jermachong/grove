# Grove - Technical Electives Course Map CLI

```


 ░████████ ░██░████  ░███████  ░██    ░██  ░███████
░██    ░██ ░███     ░██    ░██ ░██    ░██ ░██    ░██
░██    ░██ ░██      ░██    ░██  ░██  ░██  ░█████████
░██   ░███ ░██      ░██    ░██   ░██░██   ░██
 ░█████░██ ░██       ░███████     ░███     ░███████
       ░██
 ░███████

```

A powerful command-line tool for analyzing technical elective courses, checking prerequisites, and planning your academic path. Parse PDF course catalogs and find eligible courses based on your completed coursework.

## Features

- **Course Parsing**: Extract and organize course data from PDF catalogs
- **Smart Search**: Find courses by keyword, major, or academic level
- **Prerequisite Checking**: Automatically determine which courses you're eligible for
- **Statistics**: Get comprehensive statistics about available courses
- **CSV Export**: Export filtered results for further analysis
- **Colored Output**: Easy-to-read terminal output with color coding
- **Academic Level Filtering**: Separate undergraduate and graduate courses

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Virtual environment (recommended)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/jermachong/grove.git
   cd grove
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv grove_env
   source grove_env/bin/activate  # On Windows: grove_env\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Verify installation:

   ```bash
   python3 grove.py --help
   ```

### Usage

Use Grove with Python:

```bash
# Show help
python3 grove.py --help

# Basic usage - show all courses with statistics
python3 grove.py courses.pdf --stats

# Filter by major and academic level
python3 grove.py courses.pdf --major CpE --undergrad

# Check courses with completed coursework
python3 grove.py courses.pdf --course-history my_courses.txt --verbose

# Generate statistics and export to CSV
python3 grove.py courses.pdf --stats --output results.csv
```

## Command Line Options

```
positional arguments:
  pdf_file              Path to the course catalog PDF file

options:
  -h, --help            Show help message and exit
  -u, --undergrad       Show only undergraduate courses
  -g, --graduate        Show only graduate courses
  -m, --major {EE,CpE,CS,IT,EE2,CpE1,EE3}
                        Filter by major
  -ch, --course-history COURSE_HISTORY
                        File containing completed courses
  -v, --verbose         Show detailed course information
  -s, --stats           Show course statistics
  --output OUTPUT       Export results to CSV file
```

## Completed Courses File Format

Create a text file listing your completed courses:

**One per line:**

```
EEL 3123C
EEL 3801C
EEE 3342C
COP 3503C
```

**Comma-separated:**

```
EEL 3123C, EEL 3801C, EEE 3342C, COP 3503C, EGN 3211
```

## Examples

### Check CpE Undergraduate Courses with Course History

```bash
python3 grove.py courses.pdf --course-history my_courses.txt --major CpE --undergrad --verbose
```

### Generate Complete Course Statistics

```bash
python3 grove.py courses.pdf --stats --output course_analysis.csv
```

### View All Courses with Detailed Information

```bash
python3 grove.py courses.pdf --verbose
```

## Output Features

- **Color-coded status**: [OK] Success, [X] Error, [!] Warning
- **Formatted tables**: Clean, aligned course information
- **Prerequisite parsing**: Automatically extracts and displays prerequisites
- **Eligibility checking**: Shows which courses you can take based on completed work
- **CSV export**: Export filtered results for spreadsheet analysis

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
source grove_env/bin/activate
pip install -r requirements.txt
```

### Python Path Issues

If you get command not found errors, use the full path:

```bash
python3 /path/to/grove.py courses.pdf --help
```

### PDF Parsing Issues

Ensure your PDF file is readable and contains structured course information. The tool expects course codes in formats like "EEL 3123C" or "CAP 4630".

## Development

For advanced features and web-based visualization, check out the `feature/web-ui` branch which includes:

- Interactive course dependency graphs
- Modern web interface
- Flask REST API
- Real-time filtering and search

## Contributing

This tool was developed to help students navigate technical elective requirements. Feel free to:

- Report bugs or issues
- Suggest new features
- Contribute improvements
- Share with other students

## License

This project is released for educational use. Please respect your institution's academic policies when using this tool.

---

**Happy Course Planning!**
