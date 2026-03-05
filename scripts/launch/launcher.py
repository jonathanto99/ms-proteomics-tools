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

# Add backend to path
backend_path = Path(__file__).parent / 'programs' / 'mspp_web' / 'backend'
sys.path.insert(0, str(backend_path))

from app import app


def main():
    """Parse arguments and launch the app with appropriate configuration."""
    parser = argparse.ArgumentParser(
        description='MSPP Data Plotter - Launch the application',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launcher.py                # Run in development mode
  python launcher.py --prod         # Run in production mode
  python launcher.py --dev          # Explicitly run in development mode (same as default)

Environment Variables:
  FLASK_ENV      Set to 'development' or 'production'
  FLASK_HOST     Bind address (default: 127.0.0.1)
  FLASK_PORT     Port number (default: 5000)
"""
    )

    # Add mutually exclusive group for mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--prod', '--production',
        dest='mode',
        action='store_const',
        const='production',
        help='Run in production mode (no debugging)'
    )
    mode_group.add_argument(
        '--dev', '--development',
        dest='mode',
        action='store_const',
        const='development',
        help='Run in development mode with debugging (default)'
    )

    args = parser.parse_args()

    # Determine mode from argument or environment variable
    mode = args.mode or os.getenv('FLASK_ENV', 'development')
    is_production = mode.lower() in ('production', 'prod')

    # Get configuration from environment or use defaults
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', '5000'))
    debug = not is_production

    # Print startup information
    mode_label = "Production" if is_production else "Development"
    print("=" * 60)
    print(f"🚀 MSPP Data Plotter - {mode_label} Mode")
    print("=" * 60)
    print("")
    print(f"Environment: {mode_label}")
    print(f"Host: {host}:{port}")
    print(f"Debug Mode: {debug}")
    print("")

    # Start Flask server
    print("⏳ Starting backend server...")
    print("")

    try:
        app.run(host=host, port=port, debug=debug, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\n\nApp stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
