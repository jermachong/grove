#!/usr/bin/env python3
"""
Quick test to demonstrate academic level filtering
"""

import sys
sys.path.append('.')
from tech_elect_map import *

def test_academic_level_filtering():
    """Test academic level filtering functionality"""
    print("=== Academic Level Filtering Test ===\n")
    
    # Load course data
    print("Loading course data...")
    pdf_text = extract_courses_data("EE-CPE-TechnicalElectiveListSept2025[56].pdf")
    all_courses = parse_courses(pdf_text)
    print(f"Loaded {len(all_courses)} courses\n")
    
    # Count graduate vs undergraduate
    grad_courses = [c for c in all_courses if is_graduate_course(c)]
    undergrad_courses = [c for c in all_courses if not is_graduate_course(c)]
    
    print(f"Course breakdown:")
    print(f"  Total courses: {len(all_courses)}")
    print(f"  Undergraduate courses: {len(undergrad_courses)}")
    print(f"  Graduate courses: {len(grad_courses)}")
    print()
    
    # Show some examples of graduate courses
    print("Examples of Graduate Courses (5000+ level or with grad requirements):")
    grad_examples = grad_courses[:5]  # Show first 5
    for course in grad_examples:
        number_match = re.search(r'(\d{4})', course['course_code'])
        course_number = int(number_match.group(1)) if number_match else 0
        print(f"  {course['course_code']} (Level: {course_number})")
        
        # Check if it has graduate standing requirement
        if 'graduate standing' in course['full_description'].lower():
            print(f"    → Has 'graduate standing' requirement")
        print()
    
    # Show CpE breakdown
    cpe_courses = search_courses_by_major(all_courses, "CpE")
    cpe_undergrad = filter_by_academic_level(cpe_courses, 'undergraduate')
    cpe_all = filter_by_academic_level(cpe_courses, 'graduate')
    
    print(f"CpE Courses by Academic Level:")
    print(f"  All CpE courses: {len(cpe_all)}")
    print(f"  CpE undergraduate courses: {len(cpe_undergrad)}")
    print(f"  CpE graduate courses: {len(cpe_all) - len(cpe_undergrad)}")
    
    # Example completed courses for an undergraduate
    completed_courses = [
        "EEL 3801C",  # Computer Organization
        "EEE 3342C",  # Digital Systems
        "EEL 3123C"   # Networks and Systems
    ]
    
    print(f"\nExample: Undergraduate student with completed courses:")
    for course in completed_courses:
        print(f"  ✓ {course}")
    
    # Check eligibility for undergraduate vs graduate level
    undergrad_eligible = get_eligible_courses(cpe_courses, completed_courses, academic_level='undergraduate')
    grad_eligible = get_eligible_courses(cpe_courses, completed_courses, academic_level='graduate')
    
    undergrad_can_take = len([c for c in undergrad_eligible if c['prereqs_met']])
    grad_can_take = len([c for c in grad_eligible if c['prereqs_met']])
    
    print(f"\nEligibility Results:")
    print(f"  As undergraduate: {undergrad_can_take} CpE courses available")
    print(f"  As graduate: {grad_can_take} CpE courses available")
    print(f"  Additional courses with graduate standing: {grad_can_take - undergrad_can_take}")

if __name__ == "__main__":
    test_academic_level_filtering()