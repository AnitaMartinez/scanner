from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from rich.bar import Bar
from rich.columns import Columns
from rich.text import Text
from rich.align import Align
from collections import defaultdict
from collections import Counter
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
        
    # ─── Status Code Distribution Chart ────────────────────────────────────────

    status_counter = Counter()
    for entries in status_groups.values():
        for entry in entries:
            status_counter[entry["status"]] += 1

    max_count = max(status_counter.values()) if status_counter else 1

    def render_bar(count, max_count, width=30, color="cyan"):
        bar_length = int((count / max_count) * width)
        return Text("█" * bar_length, style=color)

    chart_table = Table(show_header=True, header_style="bold cyan")
    chart_table.add_column("Status Code", style="bold", width=12)
    chart_table.add_column("Bar", style="cyan")
    chart_table.add_column("Count", justify="right", width=6)

    for code, count in sorted(status_counter.items()):
        bar = render_bar(count, max_count)
        chart_table.add_row(code, bar, str(count))

    chart_panel = Panel(
        chart_table,
        title="[bold green]FFUF Status Code Summary",
        border_style="green",
        padding=(1, 2)
    )

    # ─── Combine everything in one final panel ────────────────────────────────────────

    summary_group = Group(
        *tables,
        chart_panel
    )

    console.print(Panel(summary_group, title="[bold blue]FFUF Output Summary", border_style="blue"))
    