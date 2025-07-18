import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Strip ANSI Escape Codes
# WhatWeb result is a single long string, with various plugins and metadata, using ANSI codes (like [1m) for formatting
ansi_escape = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')

def strip_ansi(text): # for ansi codes in the output
    return ansi_escape.sub('', text)

def display_whatweb_result(raw_output):
    console = Console()

    output = strip_ansi(raw_output)
    matches = re.findall(r'(\w+)\[([^\]]+)\]', output)

    if not matches:
        console.print("[bold red]No plugins detected in WhatWeb output.[/bold red]")
        return

    table = Table(
        title="🔍 WhatWeb Detected Technologies",
        box=box.SIMPLE_HEAD,
        title_style="bold green",
        show_lines=True
    )

    table.add_column("Plugin", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    for plugin, value in matches:
        if plugin.lower() in ["jquery", "html5"]:
            plugin = f"🌐 {plugin}"
        elif plugin.lower() in ["php"]:
            plugin = f"🐘 {plugin}"
        elif plugin.lower() == "apache":
            plugin = f"🔥 {plugin}"
        elif plugin.lower() in ["uncommonheaders", "x-frame-options", "ip"]:
            plugin = f"🛡️ {plugin}"
        elif plugin.lower() in ["title"]:
            plugin = f"📛 {plugin}"
        elif plugin.lower() in ["script"]:
            plugin = f"📜 {plugin}"

        table.add_row(plugin, value)

    console.print(Panel(table, title="[bold blue]WhatWeb Output Summary", border_style="blue"))
