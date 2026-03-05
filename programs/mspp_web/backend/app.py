#!/usr/bin/env python3
"""
MSPP Data Plotter - Flask Backend API

This module serves as the web interface for the Mixed Species Proteomics Performance (MSPP) tool.
It handles file uploads, session state management for uploaded proteomics data, and provides
RESTful endpoints for generating and exporting analytical visualizations.

Architecture:
- app.py: Handles HTTP requests, file persistence, and routing.
- logic.py: Contains heavy-lifting data processing and plotting logic.
"""

import contextlib
import io
import logging
import mimetypes
import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import our custom logic for data processing and visualization
from .logic import DataProcessor, PlotGenerator, fig_to_base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Force correct MIME types to ensure Vite/React assets load correctly in all environments
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

# Cross-platform path handling: use Path() for proper OS-specific path resolution
BACKEND_DIR = Path(__file__).parent
STATIC_FOLDER = str(BACKEND_DIR.parent / 'frontend' / 'dist')
TEMP_DIR = Path(os.getenv('MSPP_TEMP_DIR', tempfile.gettempdir()))

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')

# Configure CORS with environment-based origins for flexibility
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')
cors_config = {
    'origins': [origin.strip() for origin in cors_origins],
    'supports_credentials': True
}
CORS(app, resources={r'/api/*': cors_config})

# Global instances shared across the session
# Note: In a multi-user production environment, these should be session-scoped or stateless.
processor = DataProcessor()
plotter = PlotGenerator(processor)
uploaded_files = {}

@app.after_request
def add_security_headers(response):
    """
    Middleware to inject security and performance-related headers into every response.
    - Cache-Control: Prevents browsers from caching sensitive proteomics data.
    - CSP: Restricts resource loading to 'self' while allowing data: URIs for base64 plots.
    """
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:;"
    return response

@app.route('/')
def serve_react_app():
    """Serves the compiled React frontend from the /dist folder."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health')
def health_check():
    """Simple health check endpoint for monitoring or readiness probes."""
    return jsonify({'status': 'ok'})

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """
    Handles multi-file TSV/TXT uploads.
    Saves files to a temporary directory and tracks their paths in memory.
    """
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    temp_paths = []

    for file in files:
        if file and file.filename and file.filename.lower().endswith(('.tsv', '.txt')):
            # SECURITY: Use secure_filename to prevent directory traversal attacks
            safe_name = secure_filename(file.filename)
            # Use cross-platform TEMP_DIR variable instead of hardcoded path
            temp_path = TEMP_DIR / safe_name
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            file.save(temp_path)
            uploaded_files[safe_name] = str(temp_path)
            temp_paths.append(safe_name)
            logger.info(f"File uploaded: {safe_name} to {temp_path}")

    return jsonify({
        'message': f'{len(temp_paths)} files uploaded successfully',
        'files': temp_paths
    })

@app.route('/api/files', methods=['GET', 'DELETE'])
def manage_files():
    """
    GET: Returns a list of currently tracked filenames.
    DELETE: Cleans up temporary files from disk and resets internal state/cache.
    """
    if request.method == 'DELETE':
        for path in uploaded_files.values():
            with contextlib.suppress(Exception):
                Path(path).unlink(missing_ok=True)
        uploaded_files.clear()
        # Ensure the processor cache is wiped when files are deleted
        if hasattr(processor, 'cached_data'):
            processor.cached_data = None
            processor.cached_file_list = []
        return jsonify({'message': 'Cleared all files and cache'})
    return jsonify({'files': list(uploaded_files.keys())})

@app.route('/api/plot/<chart_type>', methods=['POST'])
def generate_plot(chart_type):
    """
    Generates a visualization and returns it as a base64 encoded string for UI rendering.

    Supported chart_types:
    - 'bar-chart': Protein ID distribution across organisms.
    - 'sample-comparison': Log2 intensity ratio boxplots.
    """
    if not uploaded_files:
        return jsonify({'error': 'No files uploaded'}), 400

    try:
        data = processor.load_data(list(uploaded_files.values()))
        if chart_type == 'bar-chart':
            fig = plotter.create_bar_chart_figure(data)
        elif chart_type == 'sample-comparison':
            fig = plotter.create_comparison_figure(data)
        else:
            return jsonify({'error': 'Invalid plot type'}), 400

        return jsonify({'image': fig_to_base64(fig)})
    except Exception as e:
        logging.exception(f"Plot generation failed: {e}")
        return jsonify({'error': 'Plot generation failed due to an internal error.'}), 500

@app.route('/api/export/<chart_type>', methods=['POST'])
def export_plot(chart_type):
    """
    Generates a high-resolution version of the requested plot and triggers a browser download.
    Uses 300 DPI for publication-quality output.
    """
    if not uploaded_files:
        return jsonify({'error': 'No files uploaded'}), 400

    try:
        data = processor.load_data(list(uploaded_files.values()))
        if chart_type == 'bar-chart':
            fig = plotter.create_bar_chart_figure(data, figsize=(10, 6))
            name = 'protein_id_bar_chart.png'
        elif chart_type == 'sample-comparison':
            fig = plotter.create_comparison_figure(data, figsize=(18, 16))
            name = 'intensity_ratio_comparison.png'
        else:
            return jsonify({'error': 'Invalid plot type'}), 400

        buf = io.BytesIO()
        # Save with high DPI for exporting to documents/presentations
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name=name)
    except Exception as e:
        logging.exception(f"Export failed: {e}")
        return jsonify({'error': 'Export failed due to an internal error.'}), 500

if __name__ == "__main__":
    # Cross-platform configuration via environment variables
    port = int(os.getenv('FLASK_PORT', '5000'))
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    debug_mode = os.getenv('FLASK_ENV', 'production').lower() in ('development', 'debug')
    
    logger.info(f"Starting Flask server on {host}:{port} (debug={debug_mode})")
    app.run(host=host, port=port, debug=debug_mode)
