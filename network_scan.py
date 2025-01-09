import os
import asyncio
from flask import Flask, request, jsonify
import logging
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
import netifaces
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

# Load environment variables
load_dotenv()

# Basic setup for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Flask app initialization
app = Flask(__name__)

# Redis backend setup for rate limiting
redis_client = Redis.from_url(os.getenv('REDIS_URL'))
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri= os.getenv('REDIS_URL')
)
limiter.init_app(app)


async def get_device_ip():
    """Retrieve the device IP address."""
    try:
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            if interface != 'lo':  # Ignore the loopback interface
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    ip_address = addrs[netifaces.AF_INET][0]['addr']
                    logging.info(f"Detected IP address: {ip_address}")
                    return ip_address
    except Exception as e:
        logging.error(f"Error getting device IP: {e}")
    return None


def get_target_network(ip):
    """Generate target network range from IP address."""
    ip_parts = ip.split('.')
    return f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"


async def scan_network():
    """Perform asynchronous network scanning."""
    device_ip = await get_device_ip()
    if not device_ip:
        logging.error("Could not detect device IP address.")
        return {"error": "Could not detect device IP address."}

    logging.info(f"Device IP detected: {device_ip}")
    target_network = get_target_network(device_ip)
    logging.info(f"Performing network scan on network: {target_network}")

    # Create ARP request
    arp_request = ARP(pdst=target_network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    logging.info("Sending ARP request...")

    try:
        answered_list, _ = srp(arp_request_broadcast, timeout=2, verbose=False)
    except Exception as e:
        logging.error(f"Error during ARP request: {e}")
        return {"error": f"Failed to send ARP request. Error: {e}"}

    if not answered_list:
        logging.warning("No devices found on the network.")
        return {"devices": []}

    devices = [{"ip": pkt[1].psrc, "mac": pkt[1].hwsrc} for pkt in answered_list]
    logging.info(f"Devices found: {devices}")
    return {"devices": devices}


# Route for triggering a network scan
@app.route('/api/scan', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limit specific to this route
async def api_scan():
    """API endpoint for network scanning."""
    api_key = request.headers.get('Authorization')
    expected_api_key = os.getenv('NETWORK_SCAN_API_KEY')

    if not api_key or api_key != expected_api_key:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        logging.info("API scan requested.")
        result = await scan_network()
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error during scan: {e}")
        return jsonify({"error": "Scan failed"}), 500


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
