
#!/usr/bin/env python3
"""
VAAZHA Bot Dashboard Runner
Starts the Flask web dashboard for bot management
"""

import sys
import os
import threading
import time

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dashboard import run_dashboard
from keep_alive import keep_alive

def main():
    """Main function to start the dashboard"""
    print("🌴 VAAZHA Bot Dashboard Starting...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 Dashboard Features:")
    print("   • Server Management & Overview")
    print("   • Economy System Analytics")
    print("   • Karma System Monitoring")
    print("   • User Management Tools")
    print("   • Configuration Interface")
    print("   • Real-time Statistics")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Start keep-alive server in background
    print("🌐 Starting keep-alive server...")
    keep_alive()
    
    # Give keep-alive a moment to start
    time.sleep(1)
    
    # Start the dashboard
    print("🚀 Launching dashboard on http://0.0.0.0:5000")
    print("📱 Access your dashboard at: https://your-repl-name.replit.app")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    try:
        run_dashboard()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard shutdown requested")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
    finally:
        print("🌴 VAAZHA Dashboard stopped")

if __name__ == "__main__":
    main()
