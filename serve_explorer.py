#!/usr/bin/env python3
"""
Simple HTTP server to serve the Base64 Asset Explorer
"""

import http.server
import socketserver
import webbrowser
import threading
import time
from pathlib import Path


def start_server(port=8080):
    """Start HTTP server and open browser."""
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    print(f"Serving from: {project_dir}")
    
    Handler = http.server.SimpleHTTPRequestHandler
    Handler.extensions_map.update({
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.html': 'text/html',
    })
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"🌐 Server running at: http://localhost:{port}")
            print(f"📁 Asset Explorer: http://localhost:{port}/asset_explorer.html")
            print("Press Ctrl+C to stop the server")
            
            # Open browser after a short delay
            def open_browser():
                time.sleep(1.5)
                webbrowser.open(f'http://localhost:{port}/asset_explorer.html')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use. Try a different port:")
            print(f"   python serve_explorer.py --port 8081")
        else:
            print(f"❌ Error starting server: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Serve Base64 Asset Explorer")
    parser.add_argument('--port', type=int, default=8080, help='Port to serve on (default: 8080)')
    args = parser.parse_args()
    
    start_server(args.port)