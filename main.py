import re
import subprocess
import requests
from rich.console import Console
from rich.table import Table

def is_ollama_running():
    """Checks if the Ollama server is running."""
    try:
        response = requests.get("http://localhost:11434/")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def parse_and_display_output(output):
    """Parses the benchmark output and displays it in a table."""
    console = Console()
    lines = output.strip().split('\n')

    if not lines:
        console.print("[bold red]Benchmark returned no output.[/bold red]")
        return

    # Find the header line
    header_index = -1
    for i, line in enumerate(lines):
        if 'Model' in line and 'Prompt Eval Speed' in line:
            header_index = i
            break

    if header_index == -1:
        console.print("[bold red]Could not find the benchmark result table in the output.[/bold red]")
        console.print("Full output:")
        console.print(output)
        return

    header = [h.strip() for h in re.split(r'  +', lines[header_index].strip())]
    table = Table(show_header=True, header_style="bold magenta")
    for column in header:
        table.add_column(column)

    for line in lines[header_index + 2:]: # Skip the line with dashes
        if line.strip() and not line.startswith('-'):
            row = [r.strip() for r in re.split(r'  +', line.strip())]
            # Pad the row with empty strings if it has fewer columns than the header
            while len(row) < len(header):
                row.append("")
            table.add_row(*row)

    console.print(table)


def run_benchmark():
    """Runs the llm-benchmark and displays the results in a table."""
    console = Console()

    if not is_ollama_running():
        console.print("[bold red]Error: Ollama server is not running.[/bold red]")
        console.print("Please start the Ollama server to run the benchmark.")
        return

    try:
        # Run the llm-benchmark command
        process = subprocess.run(
            ["llm_benchmark", "run"],
            capture_output=True,
            text=True,
            check=True
        )
        output = process.stdout
        parse_and_display_output(output)

    except FileNotFoundError:
        console.print("[bold red]Error: llm-benchmark command not found.[/bold red]")
        console.print("Please make sure you have installed the llm-benchmark library:")
        console.print("pip install llm-benchmark")
    except subprocess.CalledProcessError as e:
        if "pull model manifest" in e.stderr and "newer version of Ollama" in e.stderr:
            console.print("[bold red]Error: Your Ollama version is outdated.[/bold red]")
            console.print("The benchmark requires a newer version of Ollama to download the models.")
            console.print("Please download the latest version from: [link=https://ollama.com/download]https://ollama.com/download[/link]")
        else:
            console.print(f"[bold red]Error running llm-benchmark: {e}[/bold red]")
            console.print(f"Stderr: {e.stderr}")

if __name__ == '__main__':
    run_benchmark()