#!/usr/bin/env python3
"""
MSPP Data Plotter - Flask Backend API

This module serves the MSPP web application and provides analytical endpoints.
It is configured to serve the React frontend from the 'frontend/dist' directory.
"""

import logging
import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import custom logic for data processing and visualization
from .logic import DataProcessor, PlotGenerator, fig_to_base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants for path handling
BACKEND_DIR = Path(__file__).parent.absolute()
FRONTEND_DIST = (BACKEND_DIR.parent / 'frontend' / 'dist').absolute()
TEMP_DIR = Path(os.getenv('MSPP_TEMP_DIR', tempfile.gettempdir()))


def is_within_directory(base: Path, target: Path) -> bool:
    """
    Return True if the resolved target path is the same as, or is located within,
    the resolved base directory.
    """
    base_resolved = base.resolve()
    target_resolved = target.resolve()
    try:
        target_resolved.relative_to(base_resolved)
        return True
    except ValueError:
        return False


# Initialize Flask with the standard static folder configuration
app = Flask(__name__, static_folder=str(FRONTEND_DIST), static_url_path='')
CORS(app)

# Global instances for processing and plotting
processor = DataProcessor()
plotter = PlotGenerator(processor)
uploaded_files = {}

@app.route('/')
def serve_index():
    """Serves the main React application."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serves static assets or falls back to index.html for React Router."""
    static_root = Path(app.static_folder).resolve()
    full_path = static_root / path
    if is_within_directory(static_root, full_path) and full_path.is_file():
        return send_from_directory(app.static_folder, path)

    # Fallback to index.html for client-side routing, unless it's an API call
    if not path.startswith('api/'):
        return send_from_directory(app.static_folder, 'index.html')

    return jsonify({'error': 'Not found'}), 404

@app.route('/api/health')
def health_check():
    """Health check endpoint for the API."""
    return jsonify({'status': 'ok'})

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handles multi-file TSV/TXT uploads for proteomics data."""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    temp_paths = []

    for file in files:
        if file and file.filename and file.filename.lower().endswith(('.tsv', '.txt')):
            safe_name = secure_filename(file.filename)
            temp_path = TEMP_DIR / safe_name
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            file.save(temp_path)
            uploaded_files[safe_name] = str(temp_path)
            temp_paths.append(safe_name)
            logger.info(f"File uploaded: {safe_name}")

    return jsonify({
        'message': f'{len(temp_paths)} files uploaded successfully',
        'files': temp_paths
    })

@app.route('/api/files', methods=['GET', 'DELETE'])
def manage_files():
    """List or clear the currently uploaded session files."""
    if request.method == 'DELETE':
        for path in uploaded_files.values():
            try:
                Path(path).unlink(missing_ok=True)
            except Exception as e:
                logger.error(f"Failed to delete {path}: {e}")
        uploaded_files.clear()
        if hasattr(processor, 'cached_data'):
            processor.cached_data = None
        return jsonify({'message': 'Cleared all session data and cache'})
    return jsonify({'files': list(uploaded_files.keys())})

@app.route('/api/plot/<chart_type>', methods=['POST'])
def generate_plot(chart_type):
    """Generates analytical visualizations as base64 images."""
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
        logger.exception(f"Plot generation failed: {e}")
        return jsonify({'error': 'An internal error occurred while generating the plot.'}), 500

if __name__ == "__main__":
    port = int(os.getenv('FLASK_PORT', '5000'))
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    debug_mode = os.getenv('FLASK_ENV', 'production').lower() in ('development', 'debug')

    logger.info(f"Starting MSPP server on {host}:{port}")
    app.run(host=host, port=port, debug=debug_mode)
