#!/usr/bin/env python3
"""
Test script to demonstrate prerequisite parsing and checking functionality
"""

import sys
sys.path.append('.')
from tech_elect_map import *

def demo_prerequisite_checking():
    """Demonstrate how prerequisite checking works"""
    print("=== Prerequisite Checking Demo ===\n")
    
    # Load course data
    print("Loading course data...")
    pdf_text = extract_courses_data("EE-CPE-TechnicalElectiveListSept2025[56].pdf")
    all_courses = parse_courses(pdf_text)
    print(f"Loaded {len(all_courses)} courses\n")
    
    # Example completed courses
    completed_courses = [
        "EEE 3307C",  # Electronics I
        "EEE 3342C",  # Digital Systems
        "EEL 3123C",  # Networks and Systems  
        "EEL 3801C",  # Computer Organization
        "EEL 4750",   # Digital Signal Processing Fundamentals
        "EEL 3657"    # Linear Control Systems
    ]
    
    print("Example completed courses:")
    for course in completed_courses:
        print(f"  ✓ {course}")
    print()
    
    # Find some interesting courses to check
    test_courses = [
        "EEE 5378",  # CMOS Analog and Digital Circuit Design
        "EEL 4612C", # Introduction to Modern and Robust Control  
        "EEL 5513",  # Digital Signal Processing Applications
        "EEL 4783",  # Hardware Description Languages
        "CAP 4720"   # Computer Graphics
    ]
    
    print("Checking prerequisite requirements for sample courses:\n")
    
    for course_code in test_courses:
        # Find the course in our data
        course_found = None
        for course in all_courses:
            if course['course_code'] == course_code:
                course_found = course
                break
        
        if course_found:
            prereqs = parse_prerequisites(course_found['full_description'])
            prereqs_met, missing = check_prerequisites_met(prereqs, completed_courses)
            
            status = "✓ ELIGIBLE" if prereqs_met else "✗ NOT ELIGIBLE"
            print(f"{course_code} - {status}")
            print(f"  Majors: {course_found['majors']}")
            
            if prereqs:
                print(f"  Prerequisites: {', '.join(prereqs)}")
                if missing:
                    print(f"  Missing: {', '.join(missing)}")
            else:
                print(f"  Prerequisites: None")
            print()
    
    # Show eligible courses for CpE major
    print("=" * 50)
    cpe_courses = search_courses_by_major(all_courses, "CpE")
    eligible_cpe = get_eligible_courses(cpe_courses, completed_courses)
    eligible_count = len([c for c in eligible_cpe if c['prereqs_met']])
    
    print(f"CpE Courses Analysis:")
    print(f"Total CpE courses: {len(cpe_courses)}")
    print(f"Eligible with your completed courses: {eligible_count}")
    print(f"Still need prerequisites: {len(cpe_courses) - eligible_count}")

if __name__ == "__main__":
    demo_prerequisite_checking()