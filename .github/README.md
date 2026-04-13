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

```

## Launch the App

### Quick Start (Easiest Method)

After setup, launch the MSPP Desktop App using one of these methods:

**Windows:**
- Double-click `scripts/launch/Launch_MSPP_App.bat` (or the appropriate launcher)

**macOS/Linux:**
```bash
chmod +x scripts/launch/Launch_MSPP_App.sh
./scripts/launch/Launch_MSPP_App.sh
```

**Any Platform (Python):**
```bash
# Launch desktop app
python programs/mspp_app/gui_app.py
```

The app will open as a desktop window for analyzing proteomics data.

### Manual Launch

If you prefer to run the app manually:

```bash
# Activate environment first
source .venv/bin/activate  # macOS/Linux
# or
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Run the desktop application
python programs/mspp_app/gui_app.py
```

## Platform Support

This project is **fully cross-platform** and works on Windows, macOS, and Linux.

**Cross-Platform Features:**
- ✅ Multiple setup scripts: PowerShell (Windows), Bash (macOS/Linux), and Python (all platforms)
- ✅ Desktop launchers: .bat (Windows), .sh (macOS/Linux), and Python (all platforms)
- ✅ Path handling: Uses `pathlib.Path` for automatic platform-specific path resolution
- ✅ Line endings: Normalized via `.gitattributes` for consistent development across OS
- ✅ Provisional: All dependencies tested on Python 3.10, 3.11, 3.12, 3.13, 3.14

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed setup and [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.

## Tools

### MSPP Desktop App
Desktop application for proteomics data visualization and analysis.

**Features:**
- File browser for TSV data loading
- Protein ID bar charts
- E.coli vs Yeast fold change analysis
- Organisms vs HeLa spike-in validation
- Grouped analysis with regex pattern matching
- Dark mode UI

**Run:**
```powershell
python programs/mspp_app/gui_app.py
```

### Additional Python Tools
Other analysis and data processing tools available in the `programs/` directory.

**Available Tools:**
- `filter_fasta_gui.py` - GUI tool for filtering FASTA files by organism patterns
- `MSPP_data_analysis.ipynb` - Jupyter notebook for advanced data analysis

**Run:**
```powershell
# FASTA Filter GUI
python programs/filter_fasta_gui.py

# Launch Jupyter notebook
jupyter notebook programs/MSPP_data_analysis.ipynb
```

## Repository Structure

```
BYU-Core-MS-Lab/
├── programs/              # Analysis tools
│   ├── mspp_app/         # MSPP Desktop Application (CustomTkinter)
│   └── Other tools       # Filter FASTA, notebooks, and utilities
├── tutorials/            # Workflow tutorials
├── documentations/       # Documentation and reference materials
├── scripts/              # Development and setup scripts
├── tests/                # Unit tests and debugging utilities
├── pyproject.toml        # Project metadata and dependencies
└── LICENSE               # Apache 2.0 License
```

## Typical Workflow

1. **Prepare Data:** Export protein groups from DIA-NN as TSV
2. **Load Files:** Use the desktop app file browser
3. **Analyze:**
   - Check protein ID counts by organism
   - Validate spike-in ratios (E.coli vs Yeast)
   - Compare organisms against HeLa median
4. **Export:** Save plots for reporting

## Troubleshooting

Encountered an issue? Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common problems and solutions:
- Python not found or broken installation
- Missing dependencies
- Virtual environment issues
- And more...

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

- [Contributing Guidelines](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Troubleshooting](TROUBLESHOOTING.md)

## License

This project is licensed under the Apache 2.0 License - see [LICENSE](../LICENSE) file.

## Links

- **GitHub:** [MSCoreLab/BYU-Core-MS-Lab](https://github.com/MSCoreLab/BYU-Core-MS-Lab)
- **BYU MS Core Facility:** [Fritz B. Burns Mass Spectrometry Core Facility](https://chembio.byu.edu/ms-facilities)
- **BYU Cancer Research Center**: [BYU Simmons Cancer Research Center](https://sccr.byu.edu)

## Recent Updates

- CustomTkinter desktop application for cross-platform compatibility
- Performance optimizations via cached data processing
- Grouped fold change analysis with pattern matching
- Dark mode UI for all visualizations
- Python 3.14 support
- Simplified codebase and development setup

---

**Maintained by:** BYU Fritz B. Burns Cancer Research Center MS Core Facility
