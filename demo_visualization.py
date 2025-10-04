#!/usr/bin/env python3
"""
Demo script to showcase the course dependency visualization system
"""

import subprocess
import time
import webbrowser
import threading
import requests
from course_api import app

def test_api_endpoints():
    """Test the API endpoints to make sure they work"""
    base_url = "http://localhost:7000"
    
    print("Testing API endpoints...")
    
    try:
        # Test stats endpoint
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Stats: {stats['total_courses']} total courses")
        else:
            print("❌ Stats endpoint failed")
        
        # Test courses endpoint
        response = requests.get(f"{base_url}/api/courses/CpE")
        if response.status_code == 200:
            courses = response.json()
            print(f"✅ CpE Courses: {len(courses)} courses found")
        else:
            print("❌ CpE courses endpoint failed")
        
        # Test graph endpoint
        response = requests.get(f"{base_url}/api/graph/CpE")
        if response.status_code == 200:
            graph = response.json()
            print(f"✅ CpE Graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
        else:
            print("❌ CpE graph endpoint failed")
        
        # Test eligibility endpoint
        test_data = {
            "completed_courses": ["EEL 3801C", "EEE 3342C"],
            "major": "CpE",
            "academic_level": "undergraduate"
        }
        response = requests.post(f"{base_url}/api/eligible", json=test_data)
        if response.status_code == 200:
            eligible = response.json()
            eligible_count = len([c for c in eligible if c['prereqs_met']])
            print(f"✅ Eligibility: {eligible_count} courses eligible with test prerequisites")
        else:
            print("❌ Eligibility endpoint failed")
            
        print("\n🎉 All API endpoints working correctly!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 7000.")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False
    
    return True

def start_server():
    """Start the Flask server"""
    print("🚀 Starting Course Dependency Visualization Server...")
    print("📍 Server will be available at: http://localhost:7000")
    print("🌐 Opening browser in 3 seconds...")
    
    # Start server in a separate thread
    def run_server():
        app.run(debug=False, host='0.0.0.0', port=7000, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(3)
    
    # Test API endpoints
    if test_api_endpoints():
        # Open browser
        webbrowser.open('http://localhost:7000')
        
        print("\n" + "="*60)
        print("🎓 COURSE DEPENDENCY VISUALIZATION SYSTEM")
        print("="*60)
        print("Features:")
        print("• 📊 Interactive course dependency graph")
        print("• 🎯 Click courses to mark as completed")
        print("• 🔍 Filter by major (EE, CpE, etc.)")
        print("• 🎓 Academic level filtering (Undergrad/Grad)")
        print("• ✅ Real-time eligibility checking")
        print("• 📈 Course statistics and progress tracking")
        print("\nInstructions:")
        print("1. Select your major and academic level")
        print("2. Enter completed courses or click on graph nodes")
        print("3. Click 'Check Eligibility' to see what you can take")
        print("4. Hover over courses for detailed information")
        print("5. Use 'Update Map' to refresh with new filters")
        print("\nColor Legend:")
        print("🟦 Blue = Completed courses")
        print("🟢 Green = Eligible to take")
        print("🔴 Red = Prerequisites missing") 
        print("🟡 Yellow = Undergraduate courses")
        print("🟣 Purple = Graduate courses")
        print("🟠 Orange = External prerequisites")
        print("\n" + "="*60)
        
        try:
            # Keep server running
            print("\n⭐ Server running! Press Ctrl+C to stop...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Shutting down server...")
    else:
        print("❌ Server startup failed")

if __name__ == "__main__":
    start_server()