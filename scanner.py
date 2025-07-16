#!/usr/bin/env python3

import subprocess
import csv
import pandas as pd
from tabulate import tabulate
import argparse
from urllib.parse import urlparse
import logging
import threading
import time
import sys

# ─── Params ──────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Web hacking toolkit that orchestrates recon and scanning tasks") # This description appears when user writes --help
parser.add_argument('-u', '--url', type=str, required=True, help="Target URL. Example: http://example.com")
parser.add_argument('-p', '--port', type=str, default="80,443", help="Target port(s), comma-separated. Default: 80,443")
args = parser.parse_args()

# ─── Globals ──────────────────────────────────────────────────────────────────
url = args.url
ports = args.port
target_ip = urlparse(url).hostname # To extract IP from the URL
results = []
spinner_running = False

# ─── Spinner ─────────────────────────────────────────────────────────────
class Spinner:
    def __init__(self, message="Processing"):
        self.spinner = ['|', '/', '-', '\\']
        self.stop_running = False
        self.thread = None
        self.message = message

    def start(self):
        self.stop_running = False
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()

    def _spin(self):
        i = 0
        while not self.stop_running:
            sys.stdout.write(f"\r{self.message} {self.spinner[i % len(self.spinner)]}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def stop(self):
        self.stop_running = True
        if self.thread is not None:
            self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")  # Clear line
        sys.stdout.flush()

# ─── Log Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scan_log.log"),
        logging.StreamHandler() # To also show the log in the terminal 
    ]
)

# ─── Tools and Commands ────────────────────────────────────────────────────────
commands = {
    # General Scanning
    "Nmap": ["nmap", "-sV", "-p", ports, target_ip],
    # Technology Fingerprint
    "WhatWeb": ["whatweb", url],
    "Wafw00f": ["wafw00f", url],
    # Directory Enumeration (brute force). Content discovery
    # Vulnerability Scanning
    "Nikto": ["nikto", "-h", url]
}

logging.info(f"Target URL: {url}")
logging.info(f"Ports to scan: {ports}")

def log_checking_codes(tool_name, result, output):
    output = output.strip()
    # Handle non-zero exit codes
    if result.returncode != 0:
        if tool_name == "Nikto":
            if "Nikto v" in output and ("+ Target" in output or "+ Server:" in output):
                logging.info(f"{tool_name} executed successfully.")
            else:
                logging.error("Nikto failed: no valid output returned.")
                return f"Error: {output}"
        else:
            logging.error(f"{tool_name} failed with exit code {result.returncode}")
            return f"Error: {output}"
    else:
        logging.info(f"{tool_name} executed successfully.")
    return output

for tool_name, cmd in commands.items():
    logging.info(f"Running {tool_name}")
    spinner = Spinner(f"Running {tool_name}")
    spinner.start()
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    spinner.stop()
    
    output = result.stdout
    output = log_checking_codes(tool_name, result, output)

    # Clean outputs
    if tool_name == "Wafw00f":
        for line in output.splitlines():
            if "No WAF detected" in line or "is behind" in line:
                output = line
                break
    elif tool_name == "WhatWeb":
        output = output.split(" ", 1)[1]
    elif tool_name == "Nmap":
        filtered_lines = []
        for line in output.splitlines():
            if not (
                line.startswith("Starting Nmap") or
                line.startswith("Nmap scan report for") or
                line.startswith("Host is up") or
                line.startswith("Service detection performed.") or
                line.startswith("Nmap done:")
            ):
                filtered_lines.append(line)
        output = "\n".join(filtered_lines).strip()

    results.append({
        "Tool": tool_name,
        "Result": output.strip()
    })

# ─── Save Results to CSV ───────────────────────────────────────────────────────
csv_filename = "scan_results.csv"
logging.info(f"Saving results to {csv_filename}")

with open("scan_results.csv", "w", newline="") as csvfile:
    fieldnames = ["Tool", "Result"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in results:
        writer.writerow(row)

# ─── Display results in a table with panda ───────────────────────────────────────────────────────────
logging.info("Reading and displaying results...")

df = pd.read_csv("scan_results.csv")
print("\n Scan Results:")
print(tabulate(df, headers='keys', tablefmt='fancy_grid'))

logging.info(f"Scan complete. Results saved to {csv_filename}")
