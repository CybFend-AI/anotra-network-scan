from flask import Flask, request, jsonify
import logging
import os  # Ortam değişkeni için os modülünü ekle

# Basic setup for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Flask app initialization
app = Flask(__name__)

# Sample function to simulate network scanning
def scan_network():
    logging.info("Performing network scan...")
    # Simulated scan result
    return {"devices": ["192.168.1.1", "192.168.1.2"]}

# Route for triggering a network scan
@app.route('/api/scan', methods=['POST'])
def api_scan():
    api_key = request.headers.get('Authorization')
    expected_api_key = os.getenv('API_KEY')

    # API anahtarlarını logla
    logging.info(f"Received API Key: {api_key}")
    logging.info(f"Expected API Key: {expected_api_key}")

    if not api_key or api_key != expected_api_key:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        logging.info("API scan requested.")
        result = scan_network()
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error during scan: {e}")
        return jsonify({"error": "Scan failed"}), 500


if __name__ == "__main__":
    # Buradaki kodu sadece Gunicorn çalıştıracak
    pass
