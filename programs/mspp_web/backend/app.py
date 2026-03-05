#!/usr/bin/env python3
"""
MSPP Data Plotter - Flask Backend API

This module serves as the web interface for the Mixed Species Proteomics Performance (MSPP) tool.
It handles file uploads, session state management for uploaded proteomics data, and provides
RESTful endpoints for generating and exporting analytical visualizations.
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
mimetypes.add_type('text/html', '.html')

# Cross-platform path handling using absolute paths
# Use os.path.abspath(os.path.dirname(__file__)) for maximum compatibility on restricted Windows
BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))
# The 'dist' folder is up one level from 'backend' in the 'frontend' directory
STATIC_FOLDER = os.path.abspath(os.path.join(BACKEND_DIR, '..', 'frontend', 'dist'))
TEMP_DIR = os.path.abspath(os.getenv('MSPP_TEMP_DIR', tempfile.gettempdir()))

logger.info(f"Static folder initialized at: {STATIC_FOLDER}")

# Initialize Flask without an automatic static folder
app = Flask(__name__, static_folder=None)

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')
cors_config = {
    'origins': [origin.strip() for origin in cors_origins],
    'supports_credentials': True
}
CORS(app, resources={r'/api/*': cors_config})

# Global instances
processor = DataProcessor()
plotter = PlotGenerator(processor)
uploaded_files = {}

@app.before_request
def log_request():
    """Log incoming requests for debugging."""
    logger.info(f"Request: {request.method} {request.path}")

@app.after_request
def add_security_headers(response):
    """Inject security and performance-related headers."""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def serve_index():
    """Serves the main entry point."""
    logger.info("Serving index.html")
    return send_from_directory(STATIC_FOLDER, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """
    Manually serves static files with enhanced diagnostics for corporate environments.
    """
    safe_path = path.replace('/', os.sep)
    full_path = os.path.abspath(os.path.join(STATIC_FOLDER, safe_path))
    
    # Security check
    if not full_path.startswith(STATIC_FOLDER):
        logger.warning(f"Security: Blocked attempt to access path outside static folder: {full_path}")
        return jsonify({'error': 'Forbidden'}), 403

    # Logic to handle potential visibility issues with .js files on corporate PCs
    exists = os.path.isfile(full_path)
    
    if not exists:
        # Diagnostic: List files in the parent directory to see what Python sees
        parent_dir = os.path.dirname(full_path)
        logger.warning(f"File not found: {path}. Checking directory visibility: {parent_dir}")
        if os.path.isdir(parent_dir):
            try:
                files_in_dir = os.listdir(parent_dir)
                logger.info(f"Files visible in {os.path.basename(parent_dir)}: {files_in_dir}")
                
                # Fuzzy matching: try to find the file case-insensitively
                requested_name = os.path.basename(full_path).lower()
                for f in files_in_dir:
                    if f.lower() == requested_name:
                        logger.info(f"Fuzzy match found: {f}. Serving this instead.")
                        return send_from_directory(parent_dir, f)
            except Exception as e:
                logger.error(f"Could not list directory: {e}")
        
        # EMERGENCY: Try to stream the file directly even if isfile() says it's not there
        # Sometimes security software blocks 'stat' but allows 'read'
        if path.endswith(('.js', '.css')):
            try:
                logger.info(f"Emergency Attempt: Force-reading {path} despite 'not found' status")
                return send_from_directory(STATIC_FOLDER, path)
            except Exception as e:
                logger.warning(f"Emergency Attempt failed for {path}: {e}")

    if exists:
        mime_type, _ = mimetypes.guess_type(full_path)
        logger.info(f"Serving file: {path} (MIME: {mime_type})")
        return send_from_directory(STATIC_FOLDER, path)

    # CRITICAL: If the request looks like an asset (JS/CSS) but wasn't found,
    # do NOT fall back to index.html. Return a 404 to avoid MIME type errors.
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.js', '.css', '.png', '.jpg', '.svg', '.ico', '.map'):
        logger.warning(f"Asset definitively not found: {path}")
        return jsonify({'error': 'Asset not found'}), 404

    # If the path is an API call, return 404
    if path.startswith('api/'):
        logger.warning(f"API Route Not Found: {path}")
        return jsonify({'error': 'API endpoint not found'}), 404
        
    # Fallback to index.html for all other routes (React Router support)
    logger.info(f"Path not found, falling back to index.html: {path}")
    return send_from_directory(STATIC_FOLDER, 'index.html')

@app.route('/api/health')
def health_check():
    """Simple health check endpoint."""
    return jsonify({'status': 'ok'})

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handles multi-file TSV/TXT uploads."""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    temp_paths = []

    for file in files:
        if file and file.filename and file.filename.lower().endswith(('.tsv', '.txt')):
            safe_name = secure_filename(file.filename)
            temp_path = os.path.join(TEMP_DIR, safe_name)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            file.save(temp_path)
            uploaded_files[safe_name] = temp_path
            temp_paths.append(safe_name)
            logger.info(f"File uploaded: {safe_name} to {temp_path}")

    return jsonify({
        'message': f'{len(temp_paths)} files uploaded successfully',
        'files': temp_paths
    })

@app.route('/api/files', methods=['GET', 'DELETE'])
def manage_files():
    """Manage uploaded files."""
    if request.method == 'DELETE':
        for path in uploaded_files.values():
            with contextlib.suppress(Exception):
                if os.path.exists(path):
                    os.remove(path)
        uploaded_files.clear()
        if hasattr(processor, 'cached_data'):
            processor.cached_data = None
            processor.cached_file_list = []
        return jsonify({'message': 'Cleared all files and cache'})
    return jsonify({'files': list(uploaded_files.keys())})

@app.route('/api/plot/<chart_type>', methods=['POST'])
def generate_plot(chart_type):
    """Generates a visualization."""
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
    """Exports a plot to PNG."""
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
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name=name)
    except Exception as e:
        logging.exception(f"Export failed: {e}")
        return jsonify({'error': 'Export failed due to an internal error.'}), 500

if __name__ == "__main__":
    port = int(os.getenv('FLASK_PORT', '5000'))
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    debug_mode = os.getenv('FLASK_ENV', 'production').lower() in ('development', 'debug')
    
    logger.info(f"Starting Flask server on {host}:{port} (debug={debug_mode})")
    app.run(host=host, port=port, debug=debug_mode)
