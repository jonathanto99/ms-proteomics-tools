# BYU MS Core Facility - Analysis Tools

Mass Spectrometry QC and analysis tools for Brigham Young University's Fritz B. Burns Cancer Research Center MS Core Facility.

## Overview

This repository contains workflows and tools for bottom-up proteomics analysis, focusing on:
- Quality control optimization for MS Core Facility operations
- Spike-in validation and fold change analysis
- Protein identification and quantification
- Data visualization for DIA-NN output

## Quick Start

### Prerequisites
- Python 3.10+ ([Download](https://www.python.org/downloads/)) - 3.14+ recommended
- Node.js 18+ ([Download](https://nodejs.org/)) - only for web app

### Installation

**Automated Setup (Recommended):**
```powershell
.\scripts\setup_dev.ps1
```

**Manual Setup:**
```powershell
# 1. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies:
pip install -e ".[dev]"                   # With dev tools (Ruff, pytest)
# Or for Jupyter notebook support:
pip install -e ".[dev,jupyter]"

# 3. (Optional) Install web app frontend
cd programs/mspp_web/frontend
npm install
```

## Launch the App

### Quick Start (Easiest Method)

After setup, launch the web app using one of these methods:

**Windows:**
- **Development:** Double-click `Launch_MSPP_App.bat`
- **Production:** Double-click `Launch_MSPP_App_Prod.bat`

**macOS/Linux:**
```bash
# Development mode (with debugging)
chmod +x Launch_MSPP_App.sh
./Launch_MSPP_App.sh

# Production mode (optimized)
./Launch_MSPP_App_Prod.sh
```

**Any Platform (Python):**
```bash
# Development mode (default)
python launcher.py

# Production mode
python launcher.py --prod
```

The launchers automatically find your Python environment and open the app at `http://localhost:5000`.

### Manual Launch

If you prefer to run the app manually:

```bash
# Activate environment first
source .venv/bin/activate  # macOS/Linux
# or
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Run the Flask backend
flask --app programs.mspp_web.backend.app run

# In another terminal, run the frontend dev server (optional)
cd programs/mspp_web/frontend
npm run dev
```

## Platform Support

This project is **fully cross-platform** and works on Windows, macOS, and Linux.

**Cross-Platform Features:**
- ✅ Multiple setup scripts: PowerShell (Windows), Bash (macOS/Linux), and Python (all platforms)
- ✅ Desktop launchers: .bat (Windows), .sh (macOS/Linux), and Python (all platforms)
- ✅ Path handling: Uses `pathlib.Path` for automatic platform-specific path resolution
- ✅ Line endings: Normalized via `.gitattributes` for consistent development across OS
- ✅ Environment variables: Configure ports, CORS origins, and temp directories
- ✅ Provisional: All dependencies tested on Python 3.10, 3.11, 3.12, 3.13, 3.14

**Configuration:**
Set environment variables to customize behavior (all optional):
```bash
# Backend
FLASK_HOST=127.0.0.1           # Default: localhost
FLASK_PORT=5000                # Default: 5000
FLASK_ENV=development          # Enable debug mode
CORS_ORIGINS=http://localhost:3000,http://localhost:5000

# Frontend
VITE_PORT=3000                 # Default: 3000
VITE_API_PROXY=http://localhost:5000  # API proxy target
```

See [.env.example](.env.example) for all options and [CONTRIBUTING.md](CONTRIBUTING.md) for detailed setup.

## Tools

### MSPP Data Plotter (Web App)
Modern web-based interface for proteomics data visualization.

**Features:**
- Drag-and-drop TSV file upload
- Protein ID bar charts
- E.coli vs Yeast fold change analysis
- Organisms vs HeLa spike-in validation
- Grouped analysis with regex pattern matching
- Dark mode UI

**Run:**
```powershell
python programs/mspp_web/launch_app.py
```

### Python Tools
Additional analysis and data processing tools available in the `programs/python/` directory.

**Available Tools:**
- `filter_fasta_gui.py` - GUI tool for filtering FASTA files by organism patterns
- `MSPP_data_analysis.ipynb` - Jupyter notebook for advanced data analysis

**Run:**
```powershell
# FASTA Filter GUI
python programs/python/filter_fasta_gui.py

# Launch Jupyter notebook
jupyter notebook programs/python/MSPP_data_analysis.ipynb
```

## Repository Structure

```
BYU-Core-MS-Lab/
├── programs/              # Analysis tools
│   ├── mspp_web/         # Web application (Flask backend + React frontend)
│   └── python/           # Python tools and scripts
├── tutorials/            # Workflow tutorials
├── documentations/       # Documentation and reference materials
├── scripts/              # Development and setup scripts
├── tests/                # Unit tests and debugging utilities
├── pyproject.toml        # Project metadata and dependencies
└── LICENSE               # Apache 2.0 License
```

## Typical Workflow

1. **Prepare Data:** Export protein groups from DIA-NN as TSV
2. **Upload Files:** Use web app or desktop GUI
3. **Analyze:**
   - Check protein ID counts by organism
   - Validate spike-in ratios (E.coli vs Yeast)
   - Compare organisms against HeLa median
4. **Export:** Save plots for reporting

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```powershell
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

## Documentation

- [FA Workflow Tutorial](tutorials/FA_Workflow_Tutorial/FA_Workflow_Tutorial.qmd)
- [Web App README](programs/mspp_web/README.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## License

This project is licensed under the Apache 2.0 License - see [LICENSE](LICENSE) file.

## Links

- **GitHub:** [MSCoreLab/BYU-Core-MS-Lab](https://github.com/MSCoreLab/BYU-Core-MS-Lab)
- **BYU MS Core Facility:** [Fritz B. Burns Cancer Research Center](https://lifesciences.byu.edu/burns-cancer-center)

## Recent Updates

- Web application with React + TypeScript frontend
- Performance optimizations (5-10x faster on cached data)
- Grouped fold change analysis with pattern matching
- Dark mode UI for all visualizations
- Python 3.14 support
- Enhanced documentation and development setup

See [CHANGELOG.md](CHANGELOG.md) for full history.

---

**Maintained by:** BYU Fritz B. Burns Cancer Research Center MS Core Facility
