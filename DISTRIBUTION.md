# Technical Electives Course Map CLI - Distribution Package

## About

A lightweight, powerful command-line tool for analyzing technical elective courses and planning your academic path. Designed for easy distribution among students.

## What's Included

- `tech_elect_map.py` - Core course parsing and analysis engine
- `tech_elect_cli.py` - Full-featured command-line interface  
- `tech_elect_map` - Shell script wrapper for easy execution
- `sample_courses.txt` - Example completed courses file
- `requirements.txt` - Python dependencies
- `README.md` - Complete documentation

## Quick Install

1. **Download** this package
2. **Setup environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   chmod +x tech_elect_map
   ```
3. **Start using:**
   ```bash
   ./tech_elect_map courses.pdf --help
   ```

## Verified Features ✅

- ✅ PDF parsing and course extraction
- ✅ Major filtering (EE, CpE, CS, IT, etc.)
- ✅ Academic level filtering (undergrad/graduate)
- ✅ Keyword search functionality
- ✅ Prerequisite checking and eligibility
- ✅ Course statistics generation
- ✅ CSV export capability
- ✅ Colored terminal output
- ✅ Cross-platform compatibility

## Example Usage

```bash
# Find eligible Computer Engineering courses
./tech_elect_map courses.pdf --completed-file my_courses.txt --eligible --major CpE

# Search for machine learning courses
./tech_elect_map courses.pdf --search "machine learning" --verbose

# Export course statistics
./tech_elect_map courses.pdf --stats --output analysis.csv
```

## Package Info

- **Size**: Lightweight (~15KB core files)
- **Dependencies**: Only PyMuPDF required
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Python**: 3.7+ compatible

**Status**: Production ready ✅