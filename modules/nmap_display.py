from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

def display_nmap_result(raw_output):
    console = Console()
    lines = raw_output.splitlines()
    service_lines = []
    fingerprint_warning = False
    fingerprint_block = []

    # Parse line by line
    for line in lines:
        line = line.strip()
        if line.startswith("PORT"):
            header = line
        elif line and "/" in line and "open" in line:
            service_lines.append(line)
        elif "service unrecognized" in line:
            fingerprint_warning = True
        elif fingerprint_warning:
            fingerprint_block.append(line)

    if not service_lines:
        console.print("[bold red]No open ports found.[/bold red]")
        return

    table = Table(show_lines=True)
    table.add_column("Port", style="cyan", no_wrap=True)
    table.add_column("State", style="green")
    table.add_column("Service", style="white")
    table.add_column("Version", style="bright_magenta")

    for entry in service_lines:
        parts = entry.split()
        port, state = parts[0], parts[1]
        service = parts[2] if len(parts) > 2 else "?"
        version = " ".join(parts[3:]) if len(parts) > 3 else "?"
        table.add_row(port, state, service, version)

    console.print(Panel(table, title="[bold color(213)]📡 Nmap Output", border_style="color(213)"))

    if fingerprint_warning and fingerprint_block:
        fingerprint_text = "\n".join(fingerprint_block[:20])  # keep it readable
        fingerprint_panel = Panel(
            Syntax(fingerprint_text, "text", theme="ansi_dark", word_wrap=True),
            title="⚠️ Unrecognized Service Fingerprint (Nmap)",
            subtitle="(Partial output shown)",
            border_style="yellow",
        )
        console.print(fingerprint_panel)


