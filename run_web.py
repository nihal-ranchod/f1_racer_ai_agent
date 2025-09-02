#!/usr/bin/env python3
"""
F1 Racer AI Agent - Web Application Launcher

This script launches the Flask web application for the F1 AI Agent.
It provides an easy way to start the web interface while keeping
the CLI functionality intact.

Usage:
    python run_web.py [--port PORT] [--debug] [--host HOST]

Examples:
    python run_web.py                    # Run on localhost:5000
    python run_web.py --port 8080        # Run on localhost:8080
    python run_web.py --debug            # Run in debug mode
    python run_web.py --host 0.0.0.0     # Accept external connections
"""

import argparse
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description='F1 Racer AI Agent Web Application')
    parser.add_argument('--port', '-p', type=int, default=5000, 
                       help='Port to run the web application on (default: 5000)')
    parser.add_argument('--host', '-H', type=str, default='127.0.0.1', 
                       help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--debug', '-d', action='store_true', 
                       help='Run in debug mode')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🏎️  F1 Racer AI Agent - Web Interface")
    print("=" * 60)
    print(f"Starting web application on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server")
    print()
    
    if args.debug:
        print("⚠️  Running in DEBUG mode - not suitable for production")
        print()
    
    try:
        from app import app
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            threaded=True
        )
    except ImportError as e:
        print(f"❌ Error importing Flask app: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down web application...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting web application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()