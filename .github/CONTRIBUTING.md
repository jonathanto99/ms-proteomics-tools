# Contributing to BYU MS Core Lab

Thank you for your interest in contributing to our mass spectrometry analysis tools!

## Getting Started

### Prerequisites
- Python 3.10 or higher (3.14+ recommended)
- Node.js 18+ (for web app development)
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

4. **For web app development**
   ```bash
   cd programs/mspp_web/frontend
   npm install
   cd ../../..
   ```

## Development Workflow

### Quick App Launch

The easiest way to run the web app locally - just double-click the appropriate launcher script:

**Windows (Development):**
- Double-click: `Launch_MSPP_App.bat`
- Sets `FLASK_ENV=development` for debugging

**Windows (Production):**
- Double-click: `Launch_MSPP_App_Prod.bat`
- Sets `FLASK_ENV=production` for optimized performance

**macOS/Linux (Development):**
```bash
chmod +x Launch_MSPP_App.sh
./Launch_MSPP_App.sh
```

**macOS/Linux (Production):**
```bash
chmod +x Launch_MSPP_App_Prod.sh
./Launch_MSPP_App_Prod.sh
```

**Cross-Platform Python Launcher (Any OS):**
```bash
# Development mode (default, with debugging)
python launcher.py

# Production mode (optimized, no debugging)
python launcher.py --prod

# Show help
python launcher.py --help
```

The launchers automatically:
- Find your Python environment (.venv, pixi, or system)
- Set appropriate environment variables
- Open the app in your default browser
- Handle errors gracefully

### Code Style

- **Python**: Follow PEP 8 guidelines
  - Use Ruff for formatting and linting: `ruff format .` and `ruff check --fix .`
  - Line length: 100 characters
  
- **TypeScript/React**: 
  - Follow TypeScript best practices
  - Use functional components with hooks
  - Keep components modular and reusable

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
# Run web app backend
python programs/mspp_web/backend/app.py

# Run web app frontend (in separate terminal)
cd programs/mspp_web/frontend
npm run dev

# Run Jupyter notebook for data analysis
jupyter notebook programs/python/MSPP_data_analysis.ipynb

# Deactivate environment when done
deactivate
```

**Frontend Development (Web App):**
```bash
cd programs/mspp_web/frontend

# Development mode (hot reload)
npm run dev

# Production build
npm run build
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

### Environment Variables

The application supports environment variables for flexible cross-platform configuration:

**Backend (Flask API):**
```bash
# Host and port
FLASK_HOST=127.0.0.1          # Default: 127.0.0.1
FLASK_PORT=5000               # Default: 5000
FLASK_ENV=development         # development|production (enables debug mode)

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5000  # Comma-separated

# Temporary directory for uploads
MSPP_TEMP_DIR=/custom/temp/path  # Default: system temp directory
```

**Frontend (Vite Dev Server):**
```bash
# Development server
VITE_PORT=3000                    # Default: 3000
VITE_API_PROXY=http://localhost:5000  # Default: http://localhost:5000
```

**Example Development Setup:**
```bash
# macOS/Linux
export FLASK_ENV=development
export FLASK_PORT=5000
export VITE_PORT=3000

# Windows (PowerShell)
$env:FLASK_ENV='development'
$env:FLASK_PORT='5000'
$env:VITE_PORT='3000'

# Windows (Command Prompt)
set FLASK_ENV=development
set FLASK_PORT=5000
set VITE_PORT=3000
```

See [.env.example](.env.example) for all available options.

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
feat: Add grouped fold change plot to web app
fix: Resolve data caching issue in backend
docs: Update API endpoint documentation
refactor: Extract boxplot styling to helper method
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
│   ├── mspp_web/      # Web application (Flask backend + React frontend)
│   └── python/        # Python tools and scripts
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
   
   # Run web app build
   cd programs/mspp_web/frontend
   npm run build
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
