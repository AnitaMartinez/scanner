#!/usr/bin/env python3

import subprocess
import csv
import pandas as pd
from tabulate import tabulate
import argparse
from urllib.parse import urlparse
import logging

# ─── Params ──────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Web hacking toolkit that orchestrates recon and scanning tasks") # This description appears when user writes --help
parser.add_argument('-u', '--url', type=str, required=True, help="Target URL. Example: http://example.com")
parser.add_argument('-p', '--port', type=str, default="80,443", help="Target port(s), comma-separated. Default: 80,443")
args = parser.parse_args()

url = args.url # TODO: make sure the url is ok (I could use parseUrl library)
ports = args.port

# ─── Log Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scan_log.log"),
        logging.StreamHandler()
    ]
)

# To extract IP from the URL
parsed_url = urlparse(url)
target_ip = parsed_url.hostname

logging.info(f"Target URL: {url}")
logging.info(f"Ports to scan: {ports}")

# ─── Tools and Commands ────────────────────────────────────────────────────────
commands = {
    # general
    "Nmap": ["nmap", "-sV", "-p", ports, target_ip], # TODO: Avoid calling sudo inside subprocess commands 
    # techs
    "WhatWeb": ["whatweb", url],
    "Wafw00f": ["wafw00f", url],
    # vulnerabilities
    "Nikto": ["nikto", "-h", url]
}

results = []

for tool_name, cmd in commands.items():
    logging.info(f"Running {tool_name}")

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        logging.info(f"{tool_name} executed successfully.")

        # Clean outputs
        if tool_name == "Wafw00f":
            ## Of the whole answer, take only the necessary ouput
            for line in output.splitlines():
                if "No WAF detected" in line or "is behind" in line:
                    output = line
                    break
        elif tool_name == "WhatWeb":
            output = output.split(" ", 1)[1]  # Remove the URL part
        
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

    except subprocess.CalledProcessError as e:
        output = f"Error: {e.output.strip()}"
        logging.error(f"{tool_name} failed with error: {output}")

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
