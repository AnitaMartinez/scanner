from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from collections import defaultdict
import re

console = Console() # necessary to render Rich objects like Panels and Tables:

def display_ffuf_result(raw_output):
    if not raw_output.strip():
        console.print("[bold yellow]No FFUF results to display.[/bold yellow]")
        return

    status_groups = defaultdict(list)

    for line in raw_output.splitlines():
        match = re.match(r'(.+?) \[Status: (\d+), Size: (\d+), Words: (\d+), Lines: (\d+)', line)
        if match:
            path, status, size, words, lines = match.groups()
            status_code = int(status)
            if 200 <= status_code < 300:
                category = "🟢 2xx Success"
            elif 300 <= status_code < 400:
                category = "🔵 3xx Redirect"
            elif 400 <= status_code < 500:
                category = "🟠 4xx Client Error"
            elif 500 <= status_code < 600:
                category = "🔴 5xx Server Error"
            else:
                category = "⚪ Other"

            status_groups[category].append({
                "path": path,
                "status": status,
                "size": size,
                "words": words,
                "lines": lines
            })

    tables = []
    for category, entries in status_groups.items():
        table = Table(title=f"{category}", style="dim", header_style="bold cyan")
        table.add_column("Path", style="white")
        table.add_column("Status", justify="center")
        table.add_column("Size", justify="right")
        table.add_column("Words", justify="right")
        table.add_column("Lines", justify="right")

        for entry in entries:
            table.add_row(
                entry["path"],
                entry["status"],
                entry["size"],
                entry["words"],
                entry["lines"]
            )

        tables.append(table)
    
    # Wrap all tables in a group and place it inside a single panel
    group = Group(*tables)
    console.print(Panel(group, title="[bold blue]FFUF Output Summary", border_style="blue"))