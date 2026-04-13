# Contributing to BYU MS Core Lab

Thank you for your interest in contributing to our mass spectrometry analysis tools!

## Getting Started

### Prerequisites
- Python 3.10 or higher (3.14+ recommended)
- Git

### Setup Development Environment

**Quick Setup (Recommended):** Use one of the automated setup scripts:

- **Windows (PowerShell):**
  ```powershell
  .\scripts\setup_dev.ps1
  ```

- **macOS/Linux (Bash):**
  ```bash
  chmod +x ./scripts/setup_dev.sh
  ./scripts/setup_dev.sh
  ```

- **All Platforms (Python):**
  ```bash
  python scripts/setup_dev.py
  ```

**Manual Setup:** If you prefer to set up manually:

1. **Clone the repository**
   ```bash
   git clone https://github.com/BYU-MS-Core-Lab/BYU-MS-Core-Automative-Proteomics-Tools.git
   cd BYU-MS-Core-Automative-Proteomics-Tools
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   
   # Windows (Command Prompt)
   .venv\Scripts\activate.bat
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Install with development tools
   pip install -e ".[dev]"
   ```

## Development Workflow

### Quick App Launch

The easiest way to run the MSPP Desktop App locally:

**Windows:**
- Double-click: `scripts/launch/Launch_MSPP_App.bat` or the appropriate launcher script

**macOS/Linux:**
```bash
chmod +x scripts/launch/Launch_MSPP_App.sh
./scripts/launch/Launch_MSPP_App.sh
```

**Cross-Platform Python (Any OS):**
```bash
# Run the desktop app
python programs/mspp_app/gui_app.py
```

The app will launch as a desktop window for data analysis.

### Code Style

- **Python**: Follow PEP 8 guidelines
  - Use Ruff for formatting and linting: `ruff format .` and `ruff check --fix .`
  - Line length: 100 characters
  - Include docstrings for all functions and classes

### Common Commands

**Environment Activation:**
```bash
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# macOS/Linux
source .venv/bin/activate
```

**Daily Development:**
```bash
# Run desktop app
python programs/mspp_app/gui_app.py

# Run Jupyter notebook for data analysis
jupyter notebook programs/MSPP_data_analysis.ipynb

# Deactivate environment when done
deactivate
```

**Code Quality:**
```bash
# Format code with Ruff
ruff format programs/

# Lint and auto-fix issues
ruff check --fix programs/

# Run tests
pytest tests/
```

## Configuration

The application uses Python configuration and environment settings. For detailed setup instructions, refer to the README and launcher scripts which handle configuration automatically.

### Docstrings

All Python functions should have docstrings:

```python
def calculate_fold_change(ecoli_data, yeast_data):
    """
    Calculate log2 fold change between E.coli and Yeast intensities.
    
    Args:
        ecoli_data: Series of E.coli protein intensities
        yeast_data: Series of Yeast protein intensities
    
    Returns:
        Array of log2 fold change values
    """
    # Implementation
```

### Testing

- Write tests for new features
- Run tests before committing: `pytest tests/`
- Aim for >80% code coverage

### Git Commit Messages

Use clear, descriptive commit messages:

```
feat: Add grouped fold change plot visualization
fix: Resolve data caching issue in processor
docs: Update setup and launch instructions
refactor: Extract plot styling to helper method
```

Prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

## Project Structure

```
BYU-Core-MS-Lab/
├── programs/           # Applications
│   ├── mspp_app/      # MSPP Desktop Application (CustomTkinter)
│   └── Other tools    # Python utilities and scripts
├── scripts/           # Development and setup scripts
├── documentations/    # Documentation and reference materials
├── tests/             # Unit tests and debugging utilities
├── tutorials/         # Workflow tutorials and guides
├── pyproject.toml     # Project metadata and dependencies
└── LICENSE            # Apache 2.0 License
```

## Pull Request Process

1. **Create a feature branch**
   ```powershell
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests if applicable
   - Update documentation

3. **Test your changes**
   ```powershell
   # Run Python tests
   pytest tests/
   ```

4. **Commit and push**
   ```powershell
   git add .
   git commit -m "feat: Your feature description"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Wait for review

## Troubleshooting

If you encounter issues during setup or development:

1. **Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions:
   - Python environment problems (missing modules, encoding errors)
   - Port conflicts
   - Dependency installation issues
   - Virtual environment activation
   - Frontend/backend communication issues

2. **Run the setup script** - Resolves most environment issues:
   ```bash
   # Windows
   .\scripts\setup_dev.ps1
   
   # macOS/Linux
   ./scripts/setup_dev.sh
   
   # Any platform
   python scripts/setup_dev.py
   ```

3. **Check the launcher output** - The app launchers provide helpful diagnostic messages if something goes wrong

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Documentation improvements
- General questions

## Code of Conduct

- Be respectful and professional
- Provide constructive feedback
- Focus on the science and code quality
- Help maintain a welcoming environment

Thank you for contributing! 🔬
