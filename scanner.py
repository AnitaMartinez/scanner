import subprocess
import csv
import pandas as pd
from tabulate import tabulate
import argparse

# params
parser = argparse.ArgumentParser(description="Web hacking toolkit that orchestrates recon and scanning tasks") # This description appears when user writes --help
parser.add_argument('-u', '--url', type=str, required=True, help="Target URL")
args = parser.parse_args()

url = args.url

commands = {
    "WhatWeb": ["whatweb", url],
    "Wafw00f": ["wafw00f", url]
}

results = []

for tool_name, cmd in commands.items():
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)

        # Clean outputs
        if tool_name == "Wafw00f":
            ## Of the whole answer, take only the necessary ouput
            for line in output.splitlines():
                if "No WAF detected" in line or "is behind" in line:
                    output = line
                    break
        elif tool_name == "WhatWeb":
            output = output.split(" ", 1)[1]  # Remove the URL part

    except subprocess.CalledProcessError as e:
        output = f"Error: {e.output.strip()}"

    results.append({
        "Tool": tool_name,
        "Result": output.strip()
    })


# Save results to CSV
with open("scan_results.csv", "w", newline="") as csvfile:
    fieldnames = ["Tool", "Result"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in results:
        writer.writerow(row)


## Print results in a table with panda
df = pd.read_csv("scan_results.csv")
print("\n Scan Results:")
print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
print("Scan complete. Results saved to scan_results.csv")
