#!/usr/bin/env python3
"""
Backend API for Technical Electives Course Dependency Visualization
Provides REST endpoints for course data, prerequisites, and eligibility checking
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
from tech_elect_map import *

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Global course data cache
course_data = None

def load_course_data():
    """Load and cache course data"""
    global course_data
    if course_data is None:
        print("Loading course data from PDF...")
        pdf_text = extract_courses_data("EE-CPE-TechnicalElectiveListSept2025[56].pdf")
        course_data = parse_courses(pdf_text)
        print(f"Loaded {len(course_data)} courses")
    return course_data

def create_course_graph():
    """Create a graph representation of courses and their dependencies"""
    courses = load_course_data()
    
    graph = {
        "nodes": [],
        "edges": []
    }
    
    # Create nodes for each course
    for course in courses:
        prereqs = parse_prerequisites(course['full_description'])
        is_grad = is_graduate_course(course)
        
        # Extract course number for positioning/grouping
        number_match = re.search(r'(\d{4})', course['course_code'])
        course_number = int(number_match.group(1)) if number_match else 4000
        
        node = {
            "id": course['course_code'],
            "label": course['course_code'],
            "title": course['full_description'][:200] + "...",
            "majors": course['majors'].split(', '),
            "prerequisites": prereqs,
            "is_graduate": is_grad,
            "level": course_number,
            "group": "graduate" if is_grad else "undergraduate"
        }
        
        graph["nodes"].append(node)
    
    # Create edges for prerequisites
    course_codes = {course['course_code'] for course in courses}
    
    for course in courses:
        prereqs = parse_prerequisites(course['full_description'])
        for prereq in prereqs:
            # Only create edge if prerequisite course exists in our dataset
            if prereq in course_codes:
                edge = {
                    "from": prereq,
                    "to": course['course_code'],
                    "arrows": "to"
                }
                graph["edges"].append(edge)
    
    return graph

@app.route('/api/courses')
def get_courses():
    """Get all courses"""
    courses = load_course_data()
    
    course_list = []
    for course in courses:
        course_info = {
            "code": course['course_code'],
            "majors": course['majors'].split(', '),
            "description": course['full_description'],
            "prerequisites": parse_prerequisites(course['full_description']),
            "is_graduate": is_graduate_course(course)
        }
        course_list.append(course_info)
    
    return jsonify(course_list)

@app.route('/api/courses/<major>')
def get_courses_by_major(major):
    """Get courses filtered by major"""
    courses = load_course_data()
    filtered = search_courses_by_major(courses, major)
    
    course_list = []
    for course in filtered:
        course_info = {
            "code": course['course_code'],
            "majors": course['majors'].split(', '),
            "description": course['full_description'],
            "prerequisites": parse_prerequisites(course['full_description']),
            "is_graduate": is_graduate_course(course)
        }
        course_list.append(course_info)
    
    return jsonify(course_list)

@app.route('/api/graph')
def get_course_graph():
    """Get course dependency graph for visualization"""
    graph = create_course_graph()
    return jsonify(graph)

@app.route('/api/graph/<major>')
def get_course_graph_by_major(major):
    """Get course dependency graph filtered by major"""
    courses = load_course_data()
    filtered_courses = search_courses_by_major(courses, major)
    
    # Create subgraph with only courses from this major
    graph = {
        "nodes": [],
        "edges": []
    }
    
    filtered_codes = {course['course_code'] for course in filtered_courses}
    
    # Add nodes for filtered courses
    for course in filtered_courses:
        prereqs = parse_prerequisites(course['full_description'])
        is_grad = is_graduate_course(course)
        
        number_match = re.search(r'(\d{4})', course['course_code'])
        course_number = int(number_match.group(1)) if number_match else 4000
        
        node = {
            "id": course['course_code'],
            "label": course['course_code'],
            "title": course['full_description'][:200] + "...",
            "majors": course['majors'].split(', '),
            "prerequisites": prereqs,
            "is_graduate": is_grad,
            "level": course_number,
            "group": "graduate" if is_grad else "undergraduate"
        }
        
        graph["nodes"].append(node)
    
    # Add edges (including prerequisites that might be outside this major)
    all_courses = load_course_data()
    all_codes = {course['course_code'] for course in all_courses}
    
    for course in filtered_courses:
        prereqs = parse_prerequisites(course['full_description'])
        for prereq in prereqs:
            if prereq in all_codes:  # Prerequisite exists in our dataset
                edge = {
                    "from": prereq,
                    "to": course['course_code'],
                    "arrows": "to"
                }
                graph["edges"].append(edge)
                
                # Add prerequisite node if not already in graph
                if prereq not in filtered_codes:
                    prereq_course = next((c for c in all_courses if c['course_code'] == prereq), None)
                    if prereq_course:
                        prereq_prereqs = parse_prerequisites(prereq_course['full_description'])
                        prereq_is_grad = is_graduate_course(prereq_course)
                        
                        number_match = re.search(r'(\d{4})', prereq)
                        prereq_number = int(number_match.group(1)) if number_match else 4000
                        
                        prereq_node = {
                            "id": prereq,
                            "label": prereq,
                            "title": prereq_course['full_description'][:200] + "...",
                            "majors": prereq_course['majors'].split(', '),
                            "prerequisites": prereq_prereqs,
                            "is_graduate": prereq_is_grad,
                            "level": prereq_number,
                            "group": "prerequisite"  # Different group for external prereqs
                        }
                        graph["nodes"].append(prereq_node)
                        filtered_codes.add(prereq)
    
    return jsonify(graph)

@app.route('/api/eligible', methods=['POST'])
def check_eligibility():
    """Check course eligibility based on completed courses"""
    data = request.get_json()
    completed_courses = data.get('completed_courses', [])
    major = data.get('major', None)
    academic_level = data.get('academic_level', 'undergraduate')
    
    courses = load_course_data()
    
    if major:
        courses = search_courses_by_major(courses, major)
    
    eligible = get_eligible_courses(courses, completed_courses, academic_level=academic_level)
    
    result = []
    for course in eligible:
        course_info = {
            "code": course['course_code'],
            "majors": course['majors'].split(', '),
            "description": course['full_description'],
            "prerequisites": course['prerequisites'],
            "prereqs_met": course['prereqs_met'],
            "missing_prereqs": course['missing_prereqs'],
            "is_graduate": course.get('is_graduate', False)
        }
        result.append(course_info)
    
    return jsonify(result)

@app.route('/api/stats')
def get_statistics():
    """Get course statistics"""
    courses = load_course_data()
    
    # Count by major
    major_counts = {}
    grad_count = 0
    undergrad_count = 0
    
    for course in courses:
        # Academic level counts
        if is_graduate_course(course):
            grad_count += 1
        else:
            undergrad_count += 1
        
        # Major counts
        majors = course['majors'].split(', ')
        for major in majors:
            major = major.strip()
            major_counts[major] = major_counts.get(major, 0) + 1
    
    stats = {
        "total_courses": len(courses),
        "undergraduate_courses": undergrad_count,
        "graduate_courses": grad_count,
        "major_counts": major_counts
    }
    
    return jsonify(stats)

# Serve static files for the frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    print("Starting Course Dependency API Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)