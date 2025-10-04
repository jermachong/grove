import pymupdf as pdf 
import re

def extract_courses_data(pdf_path):
    """Extract courses data from PDF and return structured information"""
    doc = pdf.open(pdf_path)
    all_text = ""
    
    # Extract all text from PDF pages
    for page in doc:
        text = page.get_text()
        all_text += text + "\n"
    
    doc.close()
    return all_text

def parse_courses(text):
    """Parse the course text and extract course information with majors"""
    courses = []
    
    # Split text into lines and process
    lines = text.split('\n')
    
    current_course = {}
    current_majors = ""
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Skip empty lines and page headers
        if not line or "Page" in line or "Dept. of" in line or "Last Updated" in line:
            continue
            
        # Check if line contains only major abbreviations (EE, CpE, etc.)
        if re.match(r'^(EE|CpE|EE2|CpE1|EE3)(,\s*(EE|CpE|EE2|CpE1|EE3))*\s*$', line):
            current_majors = line
            continue
        
        # Check if line starts with a course code (like EEE 5353, EEL 4140C, etc.)
        course_match = re.match(r'^([A-Z]{3}\s+\d{4}[A-Z]?)', line)
        if course_match:
            # Save previous course if exists
            if current_course and current_majors:
                current_course['majors'] = current_majors
                courses.append(current_course.copy())
            
            # Start new course
            current_course = {
                'course_code': course_match.group(1),
                'full_description': line,
                'majors': current_majors
            }
        elif current_course and line:
            # Continue building the course description
            current_course['full_description'] += " " + line
    
    # Add the last course
    if current_course and current_majors:
        current_course['majors'] = current_majors
        courses.append(current_course)
    
    return courses

def search_courses_by_major(courses, major):
    """Search for courses that include a specific major"""
    matching_courses = []
    
    for course in courses:
        if major in course['majors']:
            matching_courses.append(course)
    
    return matching_courses

def display_courses(courses, major=None):
    """Display courses in a readable format"""
    if major:
        print(f"\n=== Courses for {major} Major ===")
    else:
        print(f"\n=== All Courses ===")
    
    print(f"Found {len(courses)} courses\n")
    
    for i, course in enumerate(courses, 1):
        print(f"{i}. {course['course_code']}")
        print(f"   Majors: {course['majors']}")
        print(f"   Description: {course['full_description'][:200]}...")
        print("-" * 80)

def interactive_search(courses):
    """Interactive search function for better user experience"""
    completed_courses = []
    academic_level = 'undergraduate'  # Default to undergraduate
    
    while True:
        print("\n" + "="*60)
        print("Technical Electives Search Tool")
        print("="*60)
        print("Available majors: EE, CpE, EE2, CpE1, EE3")
        print("Commands:")
        print("  - Enter a major (e.g., 'CpE', 'EE') to search")
        print("  - 'all' to show all courses")
        print("  - 'stats' to show statistics")
        print("  - 'level' to set academic level (undergraduate/graduate)")
        print("  - 'completed' to input completed courses")
        print("  - 'eligible' to show courses you can take")
        print("  - 'eligible [major]' to show eligible courses for specific major")
        print("  - 'quit' to exit")
        
        print(f"Academic Level: {academic_level.title()}")
        if completed_courses:
            print(f"Completed courses ({len(completed_courses)}): {', '.join(completed_courses)}")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice.lower() == 'quit':
            print("Goodbye!")
            break
        elif choice.lower() == 'all':
            display_courses(courses, "All")
        elif choice.lower() == 'stats':
            show_statistics(courses)
        elif choice.lower() == 'level':
            academic_level = input_academic_level()
            print(f"Academic level set to: {academic_level.title()}")
        elif choice.lower() == 'completed':
            completed_courses = input_completed_courses()
            print(f"You have completed {len(completed_courses)} courses.")
        elif choice.lower().startswith('eligible'):
            if not completed_courses:
                print("Please input your completed courses first using 'completed' command.")
                continue
            
            parts = choice.split()
            major = parts[1] if len(parts) > 1 else None
            
            if major:
                filtered_courses = search_courses_by_major(courses, major)
                if not filtered_courses:
                    print(f"No courses found for major: {major}")
                    continue
                eligible = get_eligible_courses(filtered_courses, completed_courses, academic_level=academic_level)
                print(f"Checking eligibility for {major} courses ({academic_level} level)...")
            else:
                eligible = get_eligible_courses(courses, completed_courses, academic_level=academic_level)
                print(f"Checking eligibility for all courses ({academic_level} level)...")
            
            display_eligible_courses(eligible, show_all=False, academic_level=academic_level)
            
            # Ask if user wants to see all courses including ineligible ones
            show_all_choice = input("\nShow all courses including ineligible ones? (y/n): ").strip().lower()
            if show_all_choice == 'y':
                display_eligible_courses(eligible, show_all=True, academic_level=academic_level)
                
        else:
            matching_courses = search_courses_by_major(courses, choice)
            if matching_courses:
                display_courses(matching_courses, choice)
            else:
                print(f"No courses found for major: {choice}")

def show_statistics(courses):
    """Show statistics about the courses"""
    print(f"\n=== Course Statistics ===")
    print(f"Total courses: {len(courses)}")
    
    # Count graduate vs undergraduate courses
    grad_count = 0
    undergrad_count = 0
    for course in courses:
        if is_graduate_course(course):
            grad_count += 1
        else:
            undergrad_count += 1
    
    print(f"\nBy Academic Level:")
    print(f"  Undergraduate courses: {undergrad_count}")
    print(f"  Graduate courses: {grad_count}")
    
    # Count by major
    major_counts = {}
    for course in courses:
        majors = course['majors'].split(', ')
        for major in majors:
            major = major.strip()
            major_counts[major] = major_counts.get(major, 0) + 1
    
    print("\nCourses per major:")
    for major, count in sorted(major_counts.items()):
        print(f"  {major}: {count} courses")

def parse_prerequisites(description):
    """Extract prerequisites from course description"""
    prereqs = []
    
    # Look for "PR:" or "Prerequisite(s):" pattern
    pr_patterns = [
        r'PR:\s*([^.]+)',
        r'Prerequisite\(s\):\s*([^.]+)',
        r'Prerequisites:\s*([^.]+)'
    ]
    
    for pattern in pr_patterns:
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            prereq_text = match.group(1).strip()
            # Extract course codes (like EEE 3307C, EEL 4750, etc.)
            course_codes = re.findall(r'[A-Z]{3}\s*\d{4}[A-Z]?', prereq_text)
            prereqs.extend(course_codes)
            break
    
    return prereqs

def check_prerequisites_met(course_prereqs, completed_courses):
    """Check if prerequisites are met based on completed courses"""
    if not course_prereqs:
        return True, []
    
    missing_prereqs = []
    for prereq in course_prereqs:
        # Normalize the course code format
        normalized_prereq = re.sub(r'\s+', ' ', prereq.strip())
        found = False
        
        for completed in completed_courses:
            normalized_completed = re.sub(r'\s+', ' ', completed.strip())
            if normalized_prereq.upper() == normalized_completed.upper():
                found = True
                break
        
        if not found:
            missing_prereqs.append(prereq)
    
    return len(missing_prereqs) == 0, missing_prereqs

def is_graduate_course(course):
    """Determine if a course is graduate-level based on course number and description"""
    course_code = course['course_code']
    description = course['full_description']
    
    # Extract course number
    number_match = re.search(r'(\d{4})', course_code)
    if number_match:
        course_number = int(number_match.group(1))
        # Courses 5000+ are typically graduate level
        if course_number >= 5000:
            return True
    
    # Check for graduate standing requirement in description
    grad_indicators = [
        'graduate standing',
        'grad standing', 
        'admission to mat degree',
        'graduate student',
        'pr: graduate',
        'prerequisite: graduate'
    ]
    
    description_lower = description.lower()
    for indicator in grad_indicators:
        if indicator in description_lower:
            return True
    
    return False

def filter_by_academic_level(courses, academic_level):
    """Filter courses based on academic level (undergraduate/graduate)"""
    if academic_level.lower() == 'graduate':
        return courses  # Graduate students can take all courses
    elif academic_level.lower() == 'undergraduate':
        return [course for course in courses if not is_graduate_course(course)]
    else:
        return courses  # Default: show all courses

def get_eligible_courses(courses, completed_courses, major=None, academic_level='undergraduate'):
    """Get courses that can be taken based on completed prerequisites and academic level"""
    eligible = []
    
    # First filter by academic level
    level_filtered_courses = filter_by_academic_level(courses, academic_level)
    
    for course in level_filtered_courses:
        # Filter by major if specified
        if major and major not in course['majors']:
            continue
        
        # Parse prerequisites
        prereqs = parse_prerequisites(course['full_description'])
        
        # Check if prerequisites are met
        prereqs_met, missing = check_prerequisites_met(prereqs, completed_courses)
        
        course_info = course.copy()
        course_info['prerequisites'] = prereqs
        course_info['prereqs_met'] = prereqs_met
        course_info['missing_prereqs'] = missing
        course_info['is_graduate'] = is_graduate_course(course)
        
        eligible.append(course_info)
    
    return eligible

def input_completed_courses():
    """Allow user to input their completed courses"""
    print("\n=== Input Your Completed Courses ===")
    print("Enter course codes one by one (e.g., EEE 3307C, EEL 4750)")
    print("Type 'done' when finished, 'clear' to start over")
    
    completed = []
    
    while True:
        course = input("Enter course code (or 'done'/'clear'): ").strip()
        
        if course.lower() == 'done':
            break
        elif course.lower() == 'clear':
            completed = []
            print("Cleared all courses.")
            continue
        elif course == '':
            continue
        else:
            # Validate course code format
            if re.match(r'^[A-Z]{3}\s*\d{4}[A-Z]?$', course.upper()):
                normalized_course = re.sub(r'\s+', ' ', course.upper())
                if normalized_course not in completed:
                    completed.append(normalized_course)
                    print(f"Added: {normalized_course}")
                else:
                    print(f"Already added: {normalized_course}")
            else:
                print("Invalid format. Use format like: EEE 3307C or EEL 4750")
    
    return completed

def input_academic_level():
    """Allow user to input their academic level"""
    while True:
        print("\n=== Academic Level ===")
        print("1. Undergraduate (cannot take graduate courses)")
        print("2. Graduate (can take all courses)")
        
        choice = input("Select your level (1/2): ").strip()
        
        if choice == '1':
            return 'undergraduate'
        elif choice == '2':
            return 'graduate'
        else:
            print("Please enter 1 or 2")

def display_eligible_courses(eligible_courses, show_all=False, academic_level='undergraduate'):
    """Display eligible courses with prerequisite information"""
    if show_all:
        courses_to_show = eligible_courses
        print(f"\n=== All Courses with Prerequisite Status ===")
    else:
        courses_to_show = [c for c in eligible_courses if c['prereqs_met']]
        print(f"\n=== Courses You Can Take ===")
    
    print(f"Found {len(courses_to_show)} courses\n")
    
    for i, course in enumerate(courses_to_show, 1):
        status = "✓ ELIGIBLE" if course['prereqs_met'] else "✗ NOT ELIGIBLE"
        grad_indicator = " [GRAD]" if course.get('is_graduate', False) else ""
        print(f"{i}. {course['course_code']}{grad_indicator} - {status}")
        print(f"   Majors: {course['majors']}")
        
        if course['prerequisites']:
            print(f"   Prerequisites: {', '.join(course['prerequisites'])}")
            if not course['prereqs_met']:
                print(f"   Missing: {', '.join(course['missing_prereqs'])}")
        else:
            print(f"   Prerequisites: None")
        
        print(f"   Description: {course['full_description'][:150]}...")
        print("-" * 80)

# Main execution
if __name__ == "__main__":
    print("Loading course data from PDF...")
    
    # Extract text from PDF
    pdf_text = extract_courses_data("EE-CPE-TechnicalElectiveListSept2025[56].pdf")
    
    # Parse courses
    all_courses = parse_courses(pdf_text)
    
    print(f"Successfully loaded {len(all_courses)} courses!")
    
    # Start interactive search
    interactive_search(all_courses)
    
    # Example of direct search (you can uncomment these for quick tests)
    # cpe_courses = search_courses_by_major(all_courses, "CpE")
    # print(f"\nFound {len(cpe_courses)} CpE courses")