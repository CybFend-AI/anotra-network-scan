import os
from flask import Flask, request, jsonify
import logging
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
import socket
import netifaces
from scapy.all import conf

# Basic setup for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Flask app initialization
app = Flask(__name__)

# Set Scapy to use Layer 3 socket (instead of Layer 2)
conf.L3socket = conf.L3socket


def get_device_ip():
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
    ip_parts = ip.split('.')
    target_network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    return target_network


# Sample function to simulate network scanning
def scan_network():
    device_ip = get_device_ip()
    if not device_ip:
        logging.error("Could not detect device IP address.")
        return {"error": "Could not detect device IP address."}

    logging.info(f"Device IP detected: {device_ip}")

    target_network = get_target_network(device_ip)
    logging.info(f"Performing network scan on network: {target_network}")

    # Create an ARP request to get devices in the network
    arp_request = ARP(pdst=target_network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combine ARP request and broadcast frame
    arp_request_broadcast = broadcast / arp_request
    logging.info("Sending ARP request...")

    # Get available interfaces using netifaces
    available_interfaces = netifaces.interfaces()
    logging.info(f"Available network interfaces: {available_interfaces}")

    # Send the request and receive the response
    try:
        # If 'eth0' is not correct, replace with the correct interface name
        answered_list = srp(arp_request_broadcast, timeout=1, verbose=True, iface="Ethernet")[0]
    except Exception as e:
        logging.error(f"Error sending ARP request: {e}")
        return {"error": f"Failed to send ARP request. Error: {e}"}

    if not answered_list:
        logging.error("No devices responded to the ARP request.")
        return {"error": "No devices found on the network."}

    devices = []
    for element in answered_list:
        logging.info(f"Device found: {element[1].psrc}")
        devices.append(element[1].psrc)

    return {"devices": devices}





# Route for triggering a network scan
@app.route('/api/scan', methods=['POST'])
def api_scan():
    api_key = request.headers.get('Authorization')
    expected_api_key = os.getenv('NETWORK_SCAN_API_KEY')

    if not api_key or api_key != expected_api_key:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        logging.info("API scan requested.")

        # Perform network scan
        result = scan_network()
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error during scan: {e}")
        return jsonify({"error": "Scan failed"}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)