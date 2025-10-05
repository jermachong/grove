#!/usr/bin/env python3
r"""
Grove - Academic Course Analysis CLI
A streamlined command-line tool for analyzing technical elective courses from PDF catalogs.

      ╭─────────────────────────────────╮
      │   ____                          │
      │  / ___|_ __ _____   _____        │
      │ | |  _| '__/ _ \ \ / / _ \       │
      │ | |_| | | | (_) \ V /  __/       │
      │  \____|_|  \___/ \_/ \___|       │
      │                                 │
      │  Academic Course Planning Tool  │
      ╰─────────────────────────────────╯

Usage:
    grove [options] <pdf_file>

Examples:
    grove my_catalog.pdf
    grove university_courses.pdf --major CpE --undergrad
    grove electives.pdf --course-history my_courses.txt --verbose
    grove catalog.pdf --stats --output results.csv
"""

import argparse
import sys
import os
import csv
from pathlib import Path
import re
from typing import List, Dict, Optional, Optional, Any

# Import the core functionality from Grove's parsing engine
from grove_core import (
    extract_courses_data, parse_courses, parse_prerequisites,
    check_prerequisites_met, is_graduate_course, filter_by_academic_level,
    get_eligible_courses, search_courses_by_major
)

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colorize(text: str, color: str) -> str:
    """Add color to text if terminal supports it"""
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.ENDC}"
    return text

def show_grove_header():
    """Display the Grove ASCII art header"""
    header = f"""
{colorize('┌─────────────────────────────────────────────────────────┐', Colors.CYAN)}
{colorize('│                                                         │', Colors.CYAN)}
{colorize('│   ██████  ██████   ██████  ██    ██ ███████             │', Colors.GREEN)}
{colorize('│  ██       ██   ██ ██    ██ ██    ██ ██                  │', Colors.GREEN)}
{colorize('│  ██   ███ ██████  ██    ██ ██    ██ █████               │', Colors.GREEN)}
{colorize('│  ██    ██ ██   ██ ██    ██  ██  ██  ██                  │', Colors.GREEN)}
{colorize('│   ██████  ██   ██  ██████    ████   ███████             │', Colors.GREEN)}
{colorize('│                                                         │', Colors.CYAN)}
{colorize('│            Academic Course Planning Tool                │', Colors.YELLOW)}
{colorize('│                 Technical Electives                     │', Colors.YELLOW)}
{colorize('│                                                         │', Colors.CYAN)}
{colorize('└─────────────────────────────────────────────────────────┘', Colors.CYAN)}
"""
    print(header)

def format_prerequisites_for_display(prereq_expr) -> str:
    """Convert structured prerequisite expression to display string"""
    if not prereq_expr:
        return 'None'
    
    # For CLI display, we'll show a simplified version
    return str(prereq_expr)

def load_completed_courses(file_path: str) -> List[str]:
    """Load completed courses from a text file"""
    if not os.path.exists(file_path):
        print(f"{colorize('Error:', Colors.RED)} Completed courses file '{file_path}' not found.")
        sys.exit(1)
    
    completed = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Support both line-by-line and comma-separated formats
            # First, try to split by lines
            lines = content.strip().split('\n')
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):  # Skip empty lines and comments
                    continue
                
                # Check if line contains commas (comma-separated format)
                if ',' in line:
                    courses_in_line = [c.strip().upper() for c in line.split(',')]
                    completed.extend([c for c in courses_in_line if c])
                else:
                    # Single course per line
                    if line.upper():
                        completed.append(line.upper())
        
        # Remove duplicates while preserving order
        seen = set()
        unique_completed = []
        for course in completed:
            if course not in seen:
                seen.add(course)
                unique_completed.append(course)
        
        return unique_completed
        
    except Exception as e:
        print(f"{colorize('Error:', Colors.RED)} Failed to read completed courses file: {e}")
        sys.exit(1)

def validate_major(major: str) -> bool:
    """Validate if the major is supported"""
    valid_majors = ['EE', 'CpE', 'CS', 'IT', 'EE2', 'CpE1', 'EE3']
    return major in valid_majors

def search_courses(courses: List[Dict], query: str) -> List[Dict]:
    """Search courses by query in course code or description"""
    query_lower = query.lower()
    results = []
    
    for course in courses:
        # Search in course code
        if query_lower in course['course_code'].lower():
            results.append(course)
            continue
        
        # Search in description
        if query_lower in course['full_description'].lower():
            results.append(course)
            continue
    
    return results

def display_stats(courses: List[Dict], completed_courses: Optional[List[str]] = None):
    """Display course statistics"""
    total = len(courses)
    undergrad = len([c for c in courses if not is_graduate_course(c)])
    grad = total - undergrad
    
    # Count by major
    major_counts = {}
    for course in courses:
        majors = course['majors'].split(', ')
        for major in majors:
            major = major.strip()
            major_counts[major] = major_counts.get(major, 0) + 1
    
    print(f"\n{colorize('=== COURSE STATISTICS ===', Colors.HEADER)}")
    print(f"{colorize('Total Courses:', Colors.BOLD)} {total}")
    print(f"{colorize('Undergraduate:', Colors.BLUE)} {undergrad}")
    print(f"{colorize('Graduate:', Colors.CYAN)} {grad}")
    
    print(f"\n{colorize('Courses by Major:', Colors.BOLD)}")
    for major, count in sorted(major_counts.items()):
        print(f"  {colorize(major + ':', Colors.YELLOW)} {count}")
    
    if completed_courses:
        eligible_courses = get_eligible_courses(courses, completed_courses)
        eligible_count = len([c for c in eligible_courses if c['prereqs_met']])
        ineligible_count = len(eligible_courses) - eligible_count - len(completed_courses)
        
        print(f"\n{colorize('Your Progress:', Colors.BOLD)}")
        print(f"  {colorize('[OK] Completed:', Colors.GREEN)} {len(completed_courses)}")
        print(f"  {colorize('[OK] Eligible to take:', Colors.GREEN)} {eligible_count}")
        print(f"  {colorize('[X] Need prerequisites:', Colors.RED)} {ineligible_count}")

def display_table(courses: List[Dict], verbose: bool = False, completed_courses: Optional[List[str]] = None):
    """Display courses in table format"""
    if not courses:
        print(f"{colorize('No courses found.', Colors.YELLOW)}")
        return
    
    # All courses are displayed
    display_courses = courses
    
    # Determine eligibility status if completed courses provided
    eligibility_info = {}
    if completed_courses:
        eligible_courses = get_eligible_courses(display_courses, completed_courses)
        for course in eligible_courses:
            code = course['course_code']
            if code in completed_courses:
                eligibility_info[code] = ('[OK]', Colors.GREEN)
            elif course['prereqs_met']:
                eligibility_info[code] = ('[OK]', Colors.GREEN)
            else:
                eligibility_info[code] = ('[X]', Colors.RED)
    
    if verbose:
        # Detailed format
        print(f"\n{colorize('=== COURSE DETAILS ===', Colors.HEADER)}")
        for i, course in enumerate(display_courses, 1):
            status_symbol, status_color = eligibility_info.get(course['course_code'], ('', ''))
            
            course_title = f"{i}. {course['course_code']}"
            print(f"\n{colorize(course_title, Colors.BOLD)} {colorize(status_symbol, status_color)}")
            print(f"   {colorize('Majors:', Colors.CYAN)} {course['majors']}")
            print(f"   {colorize('Level:', Colors.CYAN)} {'Graduate' if is_graduate_course(course) else 'Undergraduate'}")
            
            prereqs = parse_prerequisites(course['full_description'])
            prereq_text = format_prerequisites_for_display(prereqs)
            print(f"   {colorize('Prerequisites:', Colors.CYAN)} {prereq_text}")
            
            # Truncate description for readability
            desc = course['full_description'][:200] + '...' if len(course['full_description']) > 200 else course['full_description']
            print(f"   {colorize('Description:', Colors.CYAN)} {desc}")
    else:
        # Simple table format
        print(f"\n{colorize('=== COURSES ===', Colors.HEADER)}")
        
        # Table headers
        headers = ['Course', 'Majors', 'Level', 'Prerequisites']
        if completed_courses:
            headers.append('Status')
        
        # Calculate column widths
        col_widths = [max(len(h), 12) for h in headers]
        for course in display_courses:
            prereqs = parse_prerequisites(course['full_description'])
            prereq_text = format_prerequisites_for_display(prereqs)
            
            widths = [
                len(course['course_code']),
                len(course['majors']),
                len('Graduate' if is_graduate_course(course) else 'Undergraduate'),
                len(prereq_text)
            ]
            
            for i, width in enumerate(widths):
                col_widths[i] = max(col_widths[i], width)
        
        # Print headers
        header_row = ' | '.join(h.ljust(w) for h, w in zip(headers, col_widths))
        print(colorize(header_row, Colors.BOLD))
        print('-' * len(header_row))
        
        # Print courses
        for course in display_courses:
            prereqs = parse_prerequisites(course['full_description'])
            prereq_text = format_prerequisites_for_display(prereqs)
            
            row_data = [
                course['course_code'].ljust(col_widths[0]),
                course['majors'].ljust(col_widths[1]),
                ('Graduate' if is_graduate_course(course) else 'Undergraduate').ljust(col_widths[2]),
                prereq_text.ljust(col_widths[3])
            ]
            
            if completed_courses:
                status_symbol, status_color = eligibility_info.get(course['course_code'], ('?', ''))
                status_text = 'Completed' if course['course_code'] in completed_courses else \
                             'Eligible' if status_symbol == '[OK]' else \
                             'Need Prereqs' if status_symbol == '[X]' else 'Unknown'
                row_data.append(colorize(status_text.ljust(col_widths[4]), status_color))
            
            print(' | '.join(row_data))

def export_to_csv(courses: List[Dict], filename: str, completed_courses: Optional[List[str]] = None):
    """Export courses to CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Course Code', 'Majors', 'Level', 'Prerequisites', 'Description']
            if completed_courses:
                fieldnames.append('Status')
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Determine eligibility if completed courses provided
            eligibility_info = {}
            if completed_courses:
                eligible_courses = get_eligible_courses(courses, completed_courses)
                for course in eligible_courses:
                    code = course['course_code']
                    if code in completed_courses:
                        eligibility_info[code] = 'Completed'
                    elif course['prereqs_met']:
                        eligibility_info[code] = 'Eligible'
                    else:
                        eligibility_info[code] = 'Need Prerequisites'
            
            for course in courses:
                prereqs = parse_prerequisites(course['full_description'])
                row = {
                    'Course Code': course['course_code'],
                    'Majors': course['majors'],
                    'Level': 'Graduate' if is_graduate_course(course) else 'Undergraduate',
                    'Prerequisites': format_prerequisites_for_display(prereqs),
                    'Description': course['full_description']
                }
                
                if completed_courses:
                    row['Status'] = eligibility_info.get(course['course_code'], 'Unknown')
                
                writer.writerow(row)
        
        print(f"{colorize('✓', Colors.GREEN)} Exported {len(courses)} courses to {colorize(filename, Colors.CYAN)}")
        
    except Exception as e:
        print(f"{colorize('Error:', Colors.RED)} Failed to export CSV: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Grove - Academic Course Analysis CLI',
        epilog="""
Examples:
  %(prog)s courses.pdf
  %(prog)s courses.pdf --major CpE --undergrad
  %(prog)s courses.pdf --course-history my_courses.txt --verbose
  %(prog)s courses.pdf --stats --output results.csv
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('pdf_file', help='Path to the course catalog PDF file (relative or absolute path)')
    
    # Academic level (mutually exclusive)
    level_group = parser.add_mutually_exclusive_group()
    level_group.add_argument('-u', '--undergrad', action='store_true',
                           help='Show only undergraduate courses')
    level_group.add_argument('-g', '--graduate', action='store_true',
                           help='Show only graduate courses')
    
    # Filtering options
    parser.add_argument('-m', '--major', choices=['EE', 'CpE', 'CS', 'IT', 'EE2', 'CpE1', 'EE3'],
                       help='Filter by major')

    
    # Prerequisites and eligibility
    parser.add_argument('-ch', '--course-history', help='File containing completed courses')

    
    # Output options
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed course information')
    parser.add_argument('-s', '--stats', action='store_true',
                       help='Show course statistics')
    parser.add_argument('--output', help='Export results to CSV file')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not os.path.exists(args.pdf_file):
        print(f"{colorize('Error:', Colors.RED)} PDF file '{args.pdf_file}' not found.")
        sys.exit(1)
    

    
    # Validate PDF file exists
    if not os.path.isfile(args.pdf_file):
        print(f"{colorize('Error:', Colors.RED)} PDF file '{args.pdf_file}' not found.")
        sys.exit(1)
    
    # Show Grove header
    show_grove_header()
    
    # Load course data
    print(f"{colorize('Loading course data from PDF...', Colors.CYAN)}")
    try:
        pdf_text = extract_courses_data(args.pdf_file)
        all_courses = parse_courses(pdf_text)
        print(f"{colorize('[OK]', Colors.GREEN)} Loaded {len(all_courses)} courses")
    except FileNotFoundError:
        print(f"{colorize('Error:', Colors.RED)} PDF file '{args.pdf_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"{colorize('Error:', Colors.RED)} Failed to load PDF: {e}")
        print(f"{colorize('Tip:', Colors.YELLOW)} Make sure the PDF contains structured course information.")
        sys.exit(1)
    
    # Load completed courses if provided
    completed_courses = []
    if args.course_history:
        completed_courses = load_completed_courses(args.course_history)
        print(f"{colorize('[OK]', Colors.GREEN)} Loaded {len(completed_courses)} completed courses")
    

    
    # Apply filters
    filtered_courses = all_courses
    
    # Filter by academic level
    if args.undergrad:
        filtered_courses = filter_by_academic_level(filtered_courses, 'undergraduate')
    elif args.graduate:
        filtered_courses = filter_by_academic_level(filtered_courses, 'graduate')
    
    # Filter by major
    if args.major:
        if args.major in ['CS', 'IT']:
            print(f"{colorize('Note:', Colors.YELLOW)} {args.major} courses not yet supported in this PDF.")
            filtered_courses = []
        else:
            filtered_courses = search_courses_by_major(filtered_courses, args.major)
    

    
    # Show statistics if requested
    if args.stats:
        display_stats(filtered_courses, completed_courses)
    
    # Display results
    if not args.stats or len(filtered_courses) > 0:
        display_table(filtered_courses, args.verbose, completed_courses)
    
    # Export to CSV if requested
    if args.output:
        export_to_csv(filtered_courses, args.output, completed_courses)

if __name__ == '__main__':
    main()