#!/usr/bin/env python3
"""
MSPP Data Plotter - Desktop Application Launcher (pywebview)
This script runs the Flask backend and opens a native OS window (WebView2 on Windows)
pointing to the local server, making it feel like a standalone desktop app.
"""

import os
import sys
import threading
import time
from pathlib import Path

# Add the backend to the Python path
project_root = Path(__file__).parent.parent.parent
backend_parent = project_root / "programs" / "mspp_web"
sys.path.insert(0, str(backend_parent))

try:
    import webview
except ImportError:
    print("Error: 'pywebview' is not installed. Please run:")
    print("  pixi add --pypi pywebview")
    sys.exit(1)

from backend.app import app


def start_flask(host, port):
    """Start the Flask server in a background thread."""
    try:
        from waitress import serve
        serve(app, host=host, port=port, _quiet=True)
    except ImportError:
        # Fallback to Flask's development server if waitress isn't available
        app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)


if __name__ == "__main__":
    # Configure connection
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "8051"))  # Use a distinct port for the desktop app
    url = f"http://{host}:{port}"

    print("=" * 60)
    print("🚀 Starting MSPP Desktop Application...")
    print("=" * 60)

    # Start Flask backend in a daemon thread so it closes when the window closes
    flask_thread = threading.Thread(target=start_flask, args=(host, port), daemon=True)
    flask_thread.start()

    # Give the server a brief moment to bind to the port
    time.sleep(1.5)

    # Create and start the native webview window
    # Note: webview.start() blocks until the window is closed
    webview.create_window(
        title="MSPP Data Plotter",
        url=url,
        width=1200,
        height=900,
        min_size=(800, 600),
        background_color="#ffffff"
    )
    
    # This runs the application loop
    webview.start()
    
    print("\n👋 Desktop application closed.")
    sys.exit(0)
