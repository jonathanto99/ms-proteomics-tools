#!/usr/bin/env python3
"""
MSPP Data Plotter - Cross-Platform Launcher
Works on Windows, macOS, and Linux with development and production modes.

Usage:
    python launcher.py [--prod|--production]     # Run in production mode
    python launcher.py [--dev|--development]     # Run in development mode (default)
    python launcher.py [--help]                   # Show this help message
"""

import argparse
import os
import sys
import webbrowser
from pathlib import Path


# Validate Python environment before importing Flask
def validate_python_environment():
    """Check if Python environment is properly configured."""
    try:
        # Try importing standard library modules that are essential
        import encodings
        import json
        import sys as sys_test
    except ModuleNotFoundError as e:
        print("\n" + "=" * 60)
        print("ERROR: Python environment is not properly configured!")
        print("=" * 60)
        print(f"\nMissing module: {e.name}")
        print("\nThis usually means:")
        print("  1. Python installation is corrupted")
        print("  2. Virtual environment wasn't activated properly")
        print("  3. System Python is broken")
        print("\nSolution:")
        print("\nRun one of these setup commands:")
        print("\n  Windows (PowerShell):")
        print("    .\\scripts\\setup_dev.ps1")
        print("\n  macOS/Linux (Bash):")
        print("    bash scripts/setup_dev.sh")
        print("\n  Any Platform (Python):")
        print("    python scripts/setup_dev.py")
        print("\nOr manually create/activate a virtual environment:")
        print("  python -m venv .venv")
        print("  .venv\\Scripts\\activate.bat  # Windows")
        print("  source .venv/bin/activate    # macOS/Linux")
        print("  pip install -e '.[dev]'")
        print("\n" + "=" * 60 + "\n")
        sys.exit(1)


# Validate environment early
validate_python_environment()

# Now safe to import Flask and other modules
# Setup Python path for proper module importing
project_root = Path(__file__).parent.parent.parent
backend_parent = project_root / "programs" / "mspp_web"

# Add the parent directory so 'backend' can be imported as a package
sys.path.insert(0, str(backend_parent))

try:
    from backend.app import app
except ImportError as e:
    print("\n" + "=" * 60)
    print("ERROR: Failed to import Flask application!")
    print("=" * 60)
    print(f"\n{e}")
    print("\nMake sure dependencies are installed:")
    print("  pip install -e '.[dev]'")
    print("\nIf the error mentions 'backend', ensure:")
    print("  - Python version is 3.10+")
    print("  - All dependencies are installed: pip install -e '.[dev]'")
    print("\n" + "=" * 60 + "\n")
    sys.exit(1)


def main():
    """Parse arguments and launch the app with appropriate configuration."""
    parser = argparse.ArgumentParser(
        description="MSPP Data Plotter - Launch the application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/launch/launcher.py                # Run in development mode
  python scripts/launch/launcher.py --prod         # Run in production mode
  python scripts/launch/launcher.py --dev          # Explicitly run in development mode (same as default)

Environment Variables:
  FLASK_ENV      Set to 'development' or 'production'
  FLASK_HOST     Bind address (default: 127.0.0.1)
  FLASK_PORT     Port number (default: 5000)
""",
    )

    # Add mutually exclusive group for mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--prod",
        "--production",
        dest="mode",
        action="store_const",
        const="production",
        help="Run in production mode (no debugging)",
    )
    mode_group.add_argument(
        "--dev",
        "--development",
        dest="mode",
        action="store_const",
        const="development",
        help="Run in development mode with debugging (default)",
    )

    args = parser.parse_args()

    # Determine mode from argument or environment variable
    mode = args.mode or os.getenv("FLASK_ENV", "development")
    is_production = mode.lower() in ("production", "prod")

    # Get configuration from environment or use defaults
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = not is_production

    # Print startup information
    mode_label = "Production" if is_production else "Development"
    print("=" * 60)
    print(f"MSPP Data Plotter - {mode_label} Mode")
    print("=" * 60)
    print("")
    print(f"Environment: {mode_label}")
    print(f"Host: {host}:{port}")
    print(f"Debug Mode: {debug}")
    print("")

    # Start Flask server
    print("Starting backend server...")
    print("")

    # Open browser after a short delay to allow server to start
    import threading
    import time

    def open_browser():
        time.sleep(2)  # Wait for server to start
        url = f"http://{host}:{port}"
        try:
            webbrowser.open(url)
            print(f"Browser opened at {url}")
        except Exception as e:
            print(f"Could not open browser automatically: {e}")
            print(f"Please manually visit: {url}")

    # Start browser in background thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    try:
        if is_production:
            try:
                from waitress import serve

                print(f"Using Waitress (production WSGI server) on {host}:{port}")
                serve(app, host=host, port=port, threads=8)
            except ImportError:
                print("\nWARNING: 'waitress' not found. Falling back to development server.")
                print("To fix: pip install waitress")
                app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)
        else:
            app.run(host=host, port=port, debug=debug, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\n\nApp stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
