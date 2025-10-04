#!/usr/bin/env python3
"""
Run the course visualization on port 5001 to avoid conflicts
"""

from course_api import app
import webbrowser
import threading
import time

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:5001')

if __name__ == '__main__':
    print("🚀 Starting Course Dependency Visualization Server on port 5001...")
    print("📍 Server will be available at: http://localhost:5001")
    print("🌐 Opening browser in 2 seconds...")
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        app.run(host='0.0.0.0', port=5001, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")