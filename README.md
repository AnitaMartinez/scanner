# WHACK - Web Hacking Automated Containerized Kit

**WHACK** is a containerized web reconnaissance and vulnerability scanning toolkit. It orchestrates multiple well-known tools to perform discovery, fingerprinting, and vulnerability checks on web targets — all from a single command.


WHACK runs the following tools automatically:

- **Nmap** – Port and service detection
- **WhatWeb** – Web technology fingerprinting
- **WafW00f** – Web Application Firewall (WAF) detection
- **Ffuf** – Content and directory brute forcing
- **Nikto** – Web server vulnerability scanning

Results are cleaned, parsed, and saved into a CSV report, with a structured summary displayed in the terminal.

##### Options:
  `-h, --help`       show this help message and exit
  `-u, --url URL`    Target URL. Example: http://example.com
  `-p, --port PORT`  Target port(s), comma-separated. Default: 80,443
  `-t, --tool TOOL`  Tools to run, comma-separated. Options: all (default), nmap, whatweb, wafwoof, ffuf, nikto

####  ⚠️ Disclaimer!!

This tool is intended for authorized testing and educational purposes only. **Do not use it against systems you don't own or have explicit permission to test**.

---

## 🚀 Usage

### 📦 Via Docker

Make sure [Docker](https://www.docker.com/) is installed on your system.

#### Pull the latest image

```bash
docker pull anitamaq/whack:latest
```

⚠️ You may need to prefix Docker commands with `sudo` depending on your system setup.

#### Run

Basic usage:

```bash
docker run -it --rm anitamaq/whack -u http://TARGET
```

With custom ports:

```bash
docker run -it --rm anitamaq/whack -u http://TARGET -p 8080,8443
```

⚠️ **Note on Localhost Targets**. When scanning services running on your local machine (e.g., http://127.0.0.1:3000), Docker cannot access localhost by default. To fix this, on Linux, use _--network host_ to give the container access to your host network (`docker run -it --rm --network host anitamaq/whack -u http://127.0.0.1:3000 -p 3000`). On Windows/macOS, _--network host_ is not supported. Instead, use your machine’s local IP address (e.g., 192.168.x.x) in the target URL.

### 🧪 Running Locally (Without Docker)

If you want to run WHACK directly on your system (not in Docker):

1. Clone the repository

```bash
git clone https://github.com/yourusername/whack.git
cd whack    
```

2. Install the required Python dependencies

```bash
pip install -r requirements.txt
```

3. Run the script

```bash
sudo python3 main.py -u http://target.com
```

⚠️ Make sure you also have the external tools (nmap, ffuf, whatweb, wafw00f, nikto) installed and available in your system.

---

## 🤝 Contributing

Pull Requests are welcome! If you have suggestions for improvements, bug fixes, or new features, feel free to fork the repo and open a PR.

For major changes or ideas, open an issue first to discuss what you’d like to do.