#!/usr/bin/env python
"""
Cross-platform development environment setup tool.
Works on Windows, macOS, and Linux.

Usage:
    python scripts/setup_dev.py
"""

import os
import platform
import subprocess
import sys
from pathlib import Path


class TerminalColors:
    """ANSI color codes for terminal output."""

    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"

    @classmethod
    def disable_on_windows(cls):
        """Disable colors on Windows if not using Windows Terminal."""
        if platform.system() == "Windows" and not os.environ.get("WT_SESSION"):
            for attr in dir(cls):
                if not attr.startswith("_"):
                    setattr(cls, attr, "")


def print_header(title: str) -> None:
    """Print a formatted header."""
    width = 50
    print(f"\n{TerminalColors.CYAN}{'=' * width}{TerminalColors.RESET}")
    print(f"{TerminalColors.CYAN}{title.center(width)}{TerminalColors.RESET}")
    print(f"{TerminalColors.CYAN}{'=' * width}{TerminalColors.RESET}\n")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{TerminalColors.GREEN}✅ {message}{TerminalColors.RESET}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"{TerminalColors.YELLOW}📋 {message}{TerminalColors.RESET}")


def print_action(message: str) -> None:
    """Print an action message."""
    print(f"{TerminalColors.YELLOW}⬇️  {message}{TerminalColors.RESET}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{TerminalColors.YELLOW}⚠️  {message}{TerminalColors.RESET}")


def run_command(cmd: list, description: str, silent: bool = False) -> tuple[bool, str]:
    """
    Run a shell command and return success status.

    Args:
        cmd: Command to run as list of strings
        description: Description of what the command does
        silent: If True, suppress output

    Returns:
        Tuple of (success, output)
    """
    try:
        kwargs = {"capture_output": silent, "text": True}
        result = subprocess.run(cmd, **kwargs, check=True)
        return True, result.stdout if silent else ""
    except subprocess.CalledProcessError as e:
        return False, str(e)
    except FileNotFoundError:
        return False, f"{cmd[0]} not found"


def check_python_version() -> bool:
    """Check if Python version is 3.10+."""
    print_info("Checking Python version...")

    version_info = sys.version_info
    version_str = f"Python {version_info.major}.{version_info.minor}.{version_info.micro}"

    if version_info >= (3, 10):
        print_success(f"{version_str} detected")
        return True
    else:
        print_warning(
            f"Python 3.10+ recommended. Found: {version_str}\n          Continue anyway? (y/n): ",
            end="",
            flush=True,
        )
        return input().lower() in ("y", "yes", "")


def create_venv() -> bool:
    """Create virtual environment if it doesn't exist."""
    print_action("Creating virtual environment...")

    venv_path = Path(".venv")
    if venv_path.exists():
        print_warning("Virtual environment already exists. Skipping...")
        return True

    success, output = run_command(
        [sys.executable, "-m", "venv", ".venv"],
        "Creating virtual environment",
    )

    if success:
        print_success("Virtual environment created")
        return True
    else:
        print(
            f"{TerminalColors.RED}❌ Failed to create virtual environment: {output}{TerminalColors.RESET}"
        )
        return False


def get_venv_python() -> str:
    """Get path to Python executable in virtual environment."""
    if platform.system() == "Windows":
        return str(Path(".venv") / "Scripts" / "python.exe")
    else:
        return str(Path(".venv") / "bin" / "python")


def upgrade_pip(python_exe: str) -> bool:
    """Upgrade pip."""
    print_action("Upgrading pip...")

    success, output = run_command(
        [python_exe, "-m", "pip", "install", "--upgrade", "pip"],
        "Upgrading pip",
        silent=True,
    )

    if success:
        print_success("pip upgraded")
        return True
    else:
        print(f"{TerminalColors.RED}❌ Failed to upgrade pip: {output}{TerminalColors.RESET}")
        return False


def install_dependencies(python_exe: str) -> bool:
    """Install Python dependencies including dev tools."""
    print_action("Installing Python dependencies (including dev tools)...")

    success, output = run_command(
        [python_exe, "-m", "pip", "install", "-e", ".[dev]"],
        "Installing dependencies",
        silent=True,
    )

    if success:
        print_success("Python dependencies installed")
        return True
    else:
        print(
            f"{TerminalColors.RED}❌ Failed to install dependencies: {output}{TerminalColors.RESET}"
        )
        return False


def check_nodejs() -> bool:
    """Check if Node.js is installed."""
    print_info("Checking Node.js...")

    result = subprocess.run(["node", "--version"], capture_output=True, text=True)
    return result.returncode == 0


def install_frontend_deps() -> bool:
    """Install frontend dependencies."""
    print_action("Installing frontend dependencies...")

    frontend_dir = Path("programs/mspp_web/frontend")
    original_cwd = os.getcwd()

    try:
        os.chdir(frontend_dir)
        success, output = run_command(
            ["npm", "install"],
            "Installing frontend dependencies",
            silent=True,
        )
        return success
    finally:
        os.chdir(original_cwd)


def print_next_steps() -> None:
    """Print next steps for the user."""
    print_header("✨ Development Environment Ready!")

    system = platform.system()

    print(f"{TerminalColors.YELLOW}Next steps:{TerminalColors.RESET}")

    if system == "Windows":
        print("  1. Activate environment: .venv\\Scripts\\Activate.ps1")
        print("  2. Or use: .venv\\Scripts\\activate.bat (cmd.exe)")
    else:
        print("  1. Activate environment: source .venv/bin/activate")

    print("  2. Run data analysis: python programs/python/MSPP_data_analysis.ipynb")
    print("  3. Run web app:")
    print("     Terminal 1: python programs/mspp_web/backend/app.py")
    print("     Terminal 2: cd programs/mspp_web/frontend && npm run dev")

    print(
        f"\n{TerminalColors.CYAN}See CONTRIBUTING.md for development guidelines{TerminalColors.RESET}\n"
    )


def main() -> int:
    """Main setup routine."""
    TerminalColors.disable_on_windows()

    print(
        f"\n{TerminalColors.CYAN}🔬 BYU MS Core Lab - Development Environment Setup{TerminalColors.RESET}"
    )
    print(f"{TerminalColors.CYAN}{'=' * 50}{TerminalColors.RESET}\n")

    # Check Python version
    if not check_python_version():
        return 1

    # Create virtual environment
    print()
    if not create_venv():
        return 1

    # Get venv Python executable
    python_exe = get_venv_python()

    # Upgrade pip
    print()
    if not upgrade_pip(python_exe):
        return 1

    # Install dependencies
    print()
    if not install_dependencies(python_exe):
        return 1

    # Check for Node.js and install frontend deps
    print()
    if check_nodejs():
        node_version = subprocess.run(
            ["node", "--version"], capture_output=True, text=True
        ).stdout.strip()
        print_success(f"Node.js {node_version} detected")

        print()
        if install_frontend_deps():
            print_success("Frontend dependencies installed")
        else:
            print_warning("Failed to install frontend dependencies")
    else:
        print_warning(
            "Node.js not found. Web app frontend will not be available.\n"
            "          Install from: https://nodejs.org/"
        )

    # Print next steps
    print_next_steps()

    return 0


if __name__ == "__main__":
    sys.exit(main())
