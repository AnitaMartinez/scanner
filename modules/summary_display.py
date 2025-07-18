from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.text import Text

console = Console()

def display_tool_summary(results):
    tool_status = {}

    for result in results:
        tool = result["Tool"]
        output = result["Result"]

        # Basic status logic
        if tool == "Nmap":
            ok = "open" in output.lower()
            message = "Found open ports" if ok else "No open ports"
        elif tool == "WhatWeb":
            ok = bool(output.strip())
            message = "Detected technologies" if ok else "No technologies detected"
        elif tool == "Wafwoof":
            ok = "is behind" in output.lower()
            message = "WAF detected" if ok else "No WAF detected"
        elif tool == "Ffuf":
            found_paths = len([line for line in output.splitlines() if "Status:" in line])
            ok = found_paths > 0
            message = f"Found {found_paths} paths" if ok else "No paths found"
        elif tool == "Nikto":
            findings = len([line for line in output.splitlines() if line.startswith("+")])
            ok = findings > 0
            message = f"Found {findings} findings" if ok else "No findings"
        else:
            ok = bool(output.strip())
            message = "Output present" if ok else "No output"

        tool_status[tool] = (ok, message)
    
    summary_tree = Tree("[bold blue]Tool Results Summary[/bold blue]")

    for tool, (ok, message) in tool_status.items():
        icon = "✅" if ok else "❌"
        tool_line = f"{tool.ljust(12, '.')} {icon}  {message}"
        summary_tree.add(Text(tool_line, style="green" if ok else "red"))

    console.print(Panel(summary_tree, border_style="blue"))
