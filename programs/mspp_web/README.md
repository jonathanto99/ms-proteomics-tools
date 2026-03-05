# MS Protein & Peptide Data Plotter (Web App)

Modern web application for analyzing and visualizing mass spectrometry proteomics data from Orbitrap Astral MS (DIA-NN output).

## Technical Architecture

This platform provides a scalable, web-based interface for proteomics analysis with clean separation of concerns.

- **Backend**: Flask REST API with modular architecture (DataProcessor + PlotGenerator classes)
- **Data Processing**: Vectorized pandas operations for high-performance analysis on large datasets
- **Visualization**: Headless Matplotlib generation (`Agg` backend) for high-DPI export without GUI dependencies
- **Performance**: In-memory stream handling (`io.BytesIO`) to eliminate disk I/O bottlenecks; instance-level caching for repeated operations
- **File Management**: Temporary directory storage with secure filename handling

## Features

### Visualizations

-   **Protein Count Bar Chart**: Stacked bar chart showing organism composition across samples
-   **Intensity Ratio Comparison**: 3-panel box plots (HeLa, E.coli, Yeast) showing log2 intensity ratios

### File Management

-   Drag-and-drop or click to upload TSV files
-   Multi-file support (E25 and E100 samples)
-   Real-time file list display
-   Clear all files with one click

### Export Options

-   Export individual plots (300 DPI PNG)
-   Export all plots as ZIP file
-   High-quality images suitable for publication

### Analysis Features

-   Automatic organism identification (HeLa, E.coli, Yeast)
-   Consensus protein calculation (proteins in both E25 and E100)
-   Log2 intensity ratio calculations
-   Quality control validation

## Quick Start

### Prerequisites

-   Python 3.14+ (or compatible)
-   Node.js 18+ and npm
-   Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Set up backend**

   ```bash
   cd backend
   pip install -e "../../../[dev]"
   ```

2. **Set up frontend**

    ``` bash
    cd frontend
    npm install
    ```

### Running the Application

#### Development Mode

**Terminal 1 - Backend:**

``` bash
cd backend
python app.py
```

Backend runs on `http://localhost:5000`

**Terminal 2 - Frontend:**

``` bash
cd frontend
npm run dev
```

Frontend runs on `http://localhost:5173`

#### Production Mode

1.  **Build frontend:**

    ``` bash
    cd frontend
    npm run build
    ```

2.  **Run backend (serves built frontend):**

    ``` bash
    cd backend
    python app.py
    ```

3.  **Access application:** Open `http://localhost:5000` in your browser

## Usage

### 1. Upload Files

-   Click the upload zone or drag-and-drop TSV files
-   Upload E25 and E100 sample files (e.g., `report.pg_matrix_E25_*.tsv` and `report.pg_matrix_E100_*.tsv`)
-   Files appear in the list below the upload zone

### 2. Generate Plots

-   Click **"Generate Protein Count Plot"** for the bar chart
-   Click **"Generate Intensity Ratio Plot"** for the comparison plots
-   Plots appear in the main viewing area

### 3. Export Results

-   **Export Current Plot**: Click the export button below the displayed plot (300 DPI PNG)
-   **Export All Plots (ZIP)**: Click the green "Export All Plots (ZIP)" button to download both plots in one archive

### 4. Clear Files

-   Click **"Clear All Files"** to remove uploaded files and start over

## Expected File Format

Input TSV files should follow DIA-NN protein group matrix format:

```         
Protein.Ids Protein.Names   Genes   First.Protein.Description   Proteotypic Protein.Q.Value Global.Q.Value  [Sample columns...]
```

**File Naming Convention:** - E25 samples: `report.pg_matrix_E25_*` - E100 samples: `report.pg_matrix_E100_*`

## Algorithm Details

### Organism Identification (Vectorized)

Protein IDs are classified using fast vectorized string matching across the entire dataset at once (preferred for files with >100k rows).

**Pattern Matching by Organism:**
- **HeLa**: `_HUMAN`, `HOMO_SAPIENS`
- **E.coli**: `_ECOLI`, `_ECOL`, `_ECO*`, `_SHIF*`, `ESCHERICHIA`
- **Yeast**: `_YEAST`, `SACCHAROMYCES`, `CEREVISIAE`
- **Unknown**: No matching pattern

See [logic.py](./backend/logic.py#L32-L45) for complete pattern definitions.

### Intensity Ratio Calculation

**Purpose**: Calculate log2(E25/E100) intensity ratios for quality control assessment.

**Algorithm Steps**:
1. **Parse filenames** to detect E25 and E100 sample pairs
2. **Find consensus proteins**: Proteins with valid, non-zero intensities in BOTH E25 and E100 samples
3. **Calculate ratios**: `log2(E25_intensity / E100_intensity)` for each consensus protein
4. **Transform**: Log transformation normalizes the distribution and makes fold-changes symmetric
5. **Filter**: Remove inf/NaN values to ensure statistical validity
6. **Visualize**: Display as box plots with median values and expected ratio reference lines

**Expected Ratio by Organism**:
- **HeLa**: ~0 (constant concentration across runs)
- **E.coli**: ~-2 (log2(25/100) = -2, represents 4-fold dilution)
- **Yeast**: ~+1 (log2(150/75) = 1, represents 2-fold concentration increase)

**Implementation Details**: See [logic.py](./backend/logic.py) for detailed docstrings explaining:
- `identify_organism_vectorized()` - Vectorized organism classification
- `calculate_intensity_ratios()` - Consensus protein filtering and ratio computation
- `calculate_sample_comparison_data()` - Sample pairing and grouping logic

## API Endpoints

**Health & File Management:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check for monitoring |
| `/api/upload` | POST | Upload TSV files (multi-file support) |
| `/api/files` | GET | List currently tracked files |
| `/api/files` | DELETE | Clear all files and cache |

**Visualization Generation:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/plot/bar-chart` | POST | Generate protein count bar chart (base64 PNG) |
| `/api/plot/sample-comparison` | POST | Generate 3-panel intensity ratio boxplots (base64 PNG) |

**Export & Download:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/export/bar-chart` | POST | Export bar chart as high-res PNG (300 DPI) |
| `/api/export/sample-comparison` | POST | Export comparison plots as high-res PNG (300 DPI) |
| `/api/export/all` | POST | Export all plots as ZIP archive |

For detailed endpoint documentation, see [app.py](./backend/app.py).

## Tech Stack

### Backend

-   **Flask**: Web framework and REST API
-   **Pandas**: Data processing and analysis
-   **NumPy**: Numerical operations
-   **Matplotlib**: Visualization generation

### Frontend

-   **React 18**: UI framework
-   **TypeScript**: Type-safe JavaScript
-   **Vite**: Build tool and dev server
-   **Lucide React**: Icon library

## Troubleshooting

### Port Already in Use

``` bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

### CORS Errors

Ensure Flask backend has CORS enabled:

``` python
from flask_cors import CORS
CORS(app)
```

### File Upload Fails

-   Check file format (must be TSV)
-   Verify file size limits in Flask config
-   Ensure files contain required columns

### Plot Not Generating

-   Verify at least one E25 and one E100 file uploaded
-   Check browser console for error messages
-   Ensure files contain required columns (Protein IDs and intensity values)
-   Verify files contain proteins from the expected organisms (HeLa, E.coli, Yeast)

## Backend Code Organization

The backend is organized into clean, modular components:

### DataProcessor (logic.py)
Handles all data ingestion, organism classification, and quantitative calculations.
- **Vectorized Operations**: Uses pandas `.str` accessor for fast pattern matching across entire datasets
- **Caching**: Caches loaded data to avoid redundant file I/O
- **Error Handling**: Graceful fallbacks when selective column loading fails

### PlotGenerator (logic.py)
Manages matplotlib visualization logic with reusable methods.
- **DRY Principle**: Single `_create_bar_chart_figure()` method used by display, individual export, and ZIP export endpoints
- **Flexible Sizing**: Figure dimensions parameterized for different use cases (web display vs. high-res export)
- **Color Consistency**: Organisms use consistent colors across all visualizations

### Flask Routes (app.py)
RESTful API endpoints with security and error handling.
- **Security Headers**: CSP, cache control, and no-store for sensitive data
- **Input Validation**: Secure filename handling to prevent directory traversal
- **Error Messages**: Helpful JSON responses with appropriate HTTP status codes

For enhanced comments and docstrings, see [app.py](./backend/app.py) and [logic.py](./backend/logic.py).

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) in the root repository.

Key guidelines for backend development:
- Follow PEP 8 style guidelines (enforced with Ruff)
- Add docstrings to all functions and classes
- Use type hints where applicable (checked with mypy)
- Run tests: `pytest tests/`
- Format code: `ruff format programs/`
- Lint: `ruff check --fix programs/`

## License

See [LICENSE](../../LICENSE) in the root repository (GPLv3).

## File Structure

```
mspp_web/
├── backend/
│   ├── app.py              # Flask API with endpoints
│   ├── logic.py            # DataProcessor and PlotGenerator classes
│   └── __pycache__/
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main React component
│   │   ├── App.css         # Styles
│   │   ├── main.tsx        # Entry point
│   │   ├── index.css       # Global styles
│   │   └── vite-env.d.ts   # TypeScript declarations
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
└── README.md
```

---

**Last Updated**: March 5, 2026

**Related Documentation**:
- [App.py](./backend/app.py) - Flask API implementation with detailed comments
- [Logic.py](./backend/logic.py) - DataProcessor and PlotGenerator with enhanced docstrings
- Main [README](../../README.md) - Repository overview
- [CHANGELOG](../../CHANGELOG.md) - Version history and refactoring details
- [CONTRIBUTING](../../CONTRIBUTING.md) - Development guidelines