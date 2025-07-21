from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def display_wafwoof_result(raw_output):
    output = raw_output.strip()
    if not output:
        console.print("[bold yellow]No Wafw00f results to display.[/bold yellow]")
        return

    # Determine what was detected
    if "No WAF detected" in output:
        msg = Text("✔️ No WAF detected", style="white")
    else:
        # WAF detected, show full output
        # Remove generic prefixes like "Powered by " if desired
        msg = Text(output, style="white")

    console.print(Panel(msg, title="[bold color(213)]🐶 Wafw00f Output", border_style="color(213)"))
