# Troubleshooting Guide

## Common Issues and Solutions

### 1. "No module named 'encodings'" or "Failed to import encodings module"

**Error Message:**
```
Fatal Python error: Failed to import encodings module
ModuleNotFoundError: No module named 'encodings'
```

**Cause:**
Your Python installation is corrupted or the system Python is not properly configured.

**Solutions:**

**Option A: Use Virtual Environment (Recommended)**
```bash
# Windows (PowerShell or Command Prompt)
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -e ".[dev]"

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Then use the launcher scripts which will automatically detect and use the virtual environment.

**Option B: Reinstall Python**
1. Download Python 3.10+ from [python.org](https://www.python.org/downloads/)
2. **Important:** Check "Add Python to PATH" during installation
3. Restart your terminal/command prompt
4. Run the setup script: `python scripts/setup_dev.py` or `.\scripts\setup_dev.ps1`

**Option C: Use Pixi (If installed)**
```bash
pixi run python launcher.py
```

---

### 2. "Python not found" Error

**Error Message:**
```
ERROR: Python not found or not properly installed!
```

**Cause:**
Python is not installed or not in your system PATH.

**Solution:**
1. Download Python 3.10+ from [python.org](https://www.python.org/downloads/)
2. **Important:** Check "Add Python to PATH" during installation
3. Close all terminal windows completely
4. Open a new terminal and run: `python --version`
5. If still not found, you may need to restart your computer

---

### 3. "No module named 'customtkinter'" or Other Missing Dependencies

**Error Message:**
```
ModuleNotFoundError: No module named 'customtkinter' (or other package)
```

**Cause:**
Dependencies are not installed in your Python environment.

**Solution:**
```bash
# Activate your environment first
# Windows
.\.venv\Scripts\activate.bat
# macOS/Linux
source .venv/bin/activate

# Then install dependencies
pip install -e ".[dev]"
```

Or use the automated setup script:
```bash
# Windows PowerShell
.\scripts\setup_dev.ps1

# macOS/Linux
bash scripts/setup_dev.sh

# Any platform
python scripts/setup_dev.py
```

---

### 4. Virtual Environment Not Activating

**Error Message:**
```
'activate' is not recognized as an internal command
```

**Cause:**
Incorrect activation command for your OS/shell.

**Solution:**

**Windows:**
```bash
# PowerShell
.\.venv\Scripts\Activate.ps1

# Command Prompt (cmd.exe)
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

If you get a permission error on macOS/Linux:
```bash
chmod +x .venv/bin/activate
source .venv/bin/activate
```

---

## Getting Help

If your issue isn't listed here:

1. **Check the logs** - The error message usually tells you what's wrong
2. **Run the setup script** - This fixes most environment issues:
   ```bash
   python scripts/setup_dev.py
   ```
3. **Check CONTRIBUTING.md** - Has more detailed setup and development info
4. **Open an issue** on GitHub with:
   - Error message (full output)
   - Operating system
   - Python version (`python --version`)
   - Steps to reproduce

---

## Quick Reference: Environment Variables

The desktop application generally uses default settings. Most functionality works without environment variable configuration. For advanced customization, refer to the launcher scripts or application source code.

---

**Last Updated:** March 5, 2026
