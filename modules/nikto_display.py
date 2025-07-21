from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
import re

console = Console()

def display_nikto_result(raw_output):
    if not raw_output.strip():
        console.print("[bold yellow]No Nikto results to display.[/bold yellow]")
        return

    findings = []

    for line in raw_output.splitlines():
        line = line.strip()
        if not line.startswith("+") or line.startswith("+-"):
            continue

        # Skip metadata like IP, Hostname, Port, Time
        if re.match(r"\+\s+(Target IP|Hostname|Port|Start Time|End Time):", line):
            continue

        # Parse real findings
        parts = line[1:].strip().split(":", 1)
        if len(parts) == 2:
            path_part, rest = parts
            path = path_part.strip()
            rest = rest.strip()

            url_match = re.search(r'(https?://\S+)', rest)
            reference = url_match.group(1) if url_match else "-"
            if reference != "-":
                description = re.sub(r'\s*See:\s*' + re.escape(reference), '', rest).strip(" .")
            else:
                description = rest.strip(" .")

            findings.append({
                "path": path,
                "description": description,
                "reference": reference
            })

    if not findings:
        console.print("[bold yellow]No vulnerabilities or findings reported by Nikto.[/bold yellow]")
        return

    table = Table(show_lines=True)
    table.add_column("Path", style="white", overflow="fold")
    table.add_column("Description", style="white", overflow="fold")
    table.add_column("Reference", style="color(213)", overflow="fold")

    for item in findings:
        table.add_row(item["path"], item["description"], item["reference"])

    group = Group(table)
    console.print(Panel(group, title="[bold color(213)]🛡️ Nikto Output", border_style="color(213)"))
