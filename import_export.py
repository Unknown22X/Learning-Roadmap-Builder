# Imports for various functionalities
import json
import time
import os 
import pandas as pd
from fpdf import FPDF
from data_manager import save_data
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from config import ROADMAP_SCHEMA
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# Initialize the rich console object for terminal output
console = Console()

# --- Utility Functions ---
def print_panel(message, subtitle="", success=True):
    border_color = "bright_green" if success else "red"
    icon = "✅" if success else "❌"
    console.print()
    if success and subtitle.startswith("File: "):
        filename = subtitle.replace("File: ", "")
        full_path = os.path.abspath(filename)
        subtitle = f"File: {full_path}"
    console.print(Panel.fit(
        f"{icon} {message}" if success else f"{icon} [red]{message}[/red]",
        subtitle=f"[dim]{subtitle}[/dim]",
        border_style=border_color,
        box=box.ROUNDED
    ))
    console.print("[dim]💡 Find your file on your Desktop or in the project folder.[/dim]")
    console.print("[dim]PDFs can be opened with any PDF viewer (e.g., Adobe Acrobat).[/dim]")
    console.print("[dim]CSVs can be opened with Excel or Google Sheets.[/dim]")

def sanitize(text):
    """Sanitizes text for FPDF compatibility."""
    return (
        text.replace("✓", "v")  # Replace checkmark with 'v'
        .replace("✗", "x")  # Replace cross with 'x'
        .encode('latin-1', 'replace')  # Encode with a safe character set
        .decode('latin-1')
    )

def validate_imported_roadmap(roadmap):
    """Validates a roadmap dictionary against a predefined schema."""
    try:
        validate(instance=roadmap, schema=ROADMAP_SCHEMA)
        return True
    except ValidationError as e:
        console.print(f"[red]Invalid roadmap JSON: {e.message}[/red]")
        return False

# --- Export Functions ---

def to_json(data, filename, idx):
    """Exports a specific roadmap to a JSON file."""
    if not filename.endswith('.json'):
        filename += '.json'
    filename = os.path.join(os.path.expanduser("~/Desktop"), filename)
    try:
        with console.status("[bold green]Exporting roadmap...[/]"):
            with open(filename, "w") as f:
                json.dump(data["roadmaps"][idx], f, indent=4)
            time.sleep(0.5)
        print_panel("Successfully exported!", f"File: {filename}", True)
        return True
    except IOError as e:
        print_panel(f"Export failed! Error: {e}", "", False)
        return False

from fpdf import FPDF

def to_pdf(data, filename, idx):
    """Exports a specific roadmap to a PDF file."""
    if not filename.endswith('.pdf'):
        filename += '.pdf'
    filename = os.path.join(os.path.expanduser("~/Desktop"), filename)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=12)
    line_height = 10
    indent = 5

    try:
        roadmap = data["roadmaps"][idx]

        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, roadmap.get('title', 'No title'), ln=True)

        # Category
        pdf.set_font("Helvetica", size=12)
        category = roadmap.get('category', 'Uncategorized')
        pdf.cell(0, 10, f"Category: {category}", ln=True)
        pdf.ln(5)

        # Steps using Courier (monospace)
        pdf.set_font("Courier", size=12)
        pdf.cell(0, 10, "Steps:", ln=True)
        pdf.ln(3)
        for step in roadmap.get("steps", []):
            done = "✓" if step.get("done") else "✗"
            done = sanitize(done)
            title = sanitize(step.get("title", ""))
            priority = step.get("priority", "")

            line = f"[{done}] {title}"
            if priority:
                line += f" (priority: {priority})"

            pdf.cell(indent)
            pdf.multi_cell(0, line_height, line)

        pdf.output(filename)

        console.print()
        console.print(Panel.fit(
            "✅ [bold green]Successfully exported![/bold green]",
            subtitle=f"[dim]File: {filename}[/dim]",
            border_style="bright_green",
            box=box.ROUNDED
        ))
        return True

    except Exception as e:
        console.print(Panel.fit(
            "❌ [red]Export failed![/red]",
            subtitle=f"[dim]Error: {str(e)}[/dim]",
            border_style="red",
            box=box.ROUNDED
        ))
        return False


def to_csv(data, filename, idx):
    """Exports a specific roadmap to a CSV file using pandas."""
    if not filename.endswith('.csv'):
        filename += '.csv'

    filename = os.path.join(os.path.expanduser("~/Desktop"), filename)

    roadmap = data["roadmaps"][idx]
    try:
        df = pd.json_normalize(
          roadmap,
          record_path='steps',
          meta=['title', 'category'],
          meta_prefix='roadmap_' ,
          errors='ignore'
            )
        df = df.rename(columns={"title": "step_title"})
        df.to_csv(filename, index=False)
        print_panel("Successfully exported!", f"File: {filename}", True)
        return True
    except Exception as e:
        console.print(f"[bold red]Failed to export CSV:[/bold red] {e}")
        return False

def to_markdown(data, filename, idx):
    """Exports a specific roadmap to a Markdown file."""
    if not filename.endswith('.md'):
        filename += '.md'
    filename = os.path.join(os.path.expanduser("~/Desktop"), filename)
    roadmap = data['roadmaps'][idx]
    md = f"# {roadmap['title']}\n\n"
    if "category" in roadmap:
        md += f"**Category:** {roadmap['category']}\n\n"
    md += "## Steps:\n"
    for step in roadmap.get("steps", []):
        done = "✓" if step.get("done") else "✗"
        title = step.get("title", "")
        priority = step.get("priority", "")
        md += f"- [{done}] {title}"
        if priority:
            md += f" _(priority: {priority})_"
        md += "\n"
    try:
        with open(filename, 'w' , encoding='utf-8') as f:
            f.write(md)
        print_panel("Successfully exported!", f"File: {filename}", True)
        
        return True
    except OSError as e:
        error_message = f"Failed to write markdown file: {e}"
        console.print(f"[bold red]{error_message}[/bold red]")
        return False

# --- User Interface Functions ---

def choose_file_type():
    """Prompts the user to select an export file type."""
    options = ["json", "pdf", "markdown", "csv"]
    try:
        table = Table(title="🗃️ File Type")
        table.add_column("#")
        table.add_column("File")
        for i, name in enumerate(options, start=1):
            table.add_row(str(i), name)
        console.print(table)
    except Exception as e:
        console.print(f"[red]❌ An error occurred: {e}[/red]")
        return None

    while True:
        try:
            choice = IntPrompt.ask(f"[bold yellow]Choose file type:[/]", choices=[str(i) for i in range(1, len(options) + 1)], show_choices=True)
            choice = int(choice)
            return options[choice - 1]
        except Exception:
            console.print("[red]Enter a valid choice[/red]")

def import_export_roadmaps(data):
    """Main function to handle the import and export menu."""
    console.clear()
    console.print(Panel.fit(
        "💾 [bold magenta]Import/Export Roadmaps[/bold magenta]",
        subtitle="[dim]Backup and share your learning journeys[/dim]",
        border_style="magenta",
        box=box.DOUBLE
    ))
    console.print()

    options_table = Table(show_header=False, box=box.SIMPLE)
    options_table.add_row("1. [bold green]📤 Export roadmap[/bold green]")
    options_table.add_row("2. [bold blue]📥 Import roadmap[/bold blue]")
    options_table.add_row("q. [dim]↩️  Back to main menu[/dim]")
    console.print(options_table)
    console.print()

    try:
        choice_input = Prompt.ask(
            "[bold]Select option[/bold]",
            choices=["1", "2", "q", "Q"],
            show_choices=False
        )
        if choice_input.lower() == 'q':
            console.print("[dim]Returning to main menu...[/dim]")
            return
        choice = int(choice_input)
    except Exception:
        console.print("[red]❌ Invalid selection![/red]")
        return

    if choice == 1:
        if not data["roadmaps"]:
            print_panel("📭 No roadmaps to export", "Create roadmaps first to export them", False)
            time.sleep(1.5)
            return

        export_table = Table(title="📤 Select Roadmap to Export (or 'q' to quit)", box=box.ROUNDED)
        export_table.add_column("#", style="bold cyan", width=4, justify="center")
        export_table.add_column("Roadmap", style="bold white")
        export_table.add_column("Steps", style="green", justify="center")
        export_table.add_column("Category", style="dim", justify="center")

        for i, roadmap in enumerate(data["roadmaps"], start=1):
            steps_count = len(roadmap.get("steps", []))
            category = roadmap.get("category", "Uncategorized")
            export_table.add_row(str(i), roadmap["title"], str(steps_count), category)

        console.print(export_table)
        console.print()

        while True:
            idx_input = Prompt.ask(
                "[bold]Select roadmap number (or 'q' to quit)[/bold]"
            )
            if idx_input.lower() == 'q':
                console.print("[dim]Export cancelled.[/dim]")
                return
            if idx_input.isdigit() and 1 <= int(idx_input) <= len(data["roadmaps"]):
                idx = int(idx_input) - 1
                break
            else:
                console.print("[red]❌ Invalid selection![/red]")

        filename = Prompt.ask("[bold]Enter export filename (or 'q' to quit) [dim]dont include the file extension[/dim][/bold]", default="roadmap")
        if filename.lower() == 'q':
            console.print("[dim]Export cancelled.[/dim]")
            return

        file_type = choose_file_type()
        if file_type is None:
            console.print("[red]❌ No valid file type selected. Export cancelled.[/red]")
            return

        result = False
        if file_type == 'json':
            result = to_json(data, filename, idx)
        elif file_type == 'pdf':
            result = to_pdf(data, filename, idx)
        elif file_type == 'csv':
            result = to_csv(data, filename, idx)
        elif file_type == 'markdown':
            result = to_markdown(data, filename, idx)

        if not result:
            console.print("[red]❌ Export failed.[/red]")

    elif choice == 2:
        filename = Prompt.ask("[bold]Enter import filename (or 'q' to quit)[/bold]")
        if filename.lower() == 'q':
            console.print("[dim]Import cancelled.[/dim]")
            return

        try:
            with console.status("[bold blue]Importing roadmap...[/]"):
                with open(filename, "r") as f:
                    roadmap = json.load(f)
                time.sleep(0.5)

            if validate_imported_roadmap(roadmap):
                data["roadmaps"].append(roadmap)
                save_data(data)
            else:
                console.print("[red]Import failed due to invalid JSON structure.[/red]")

            print_panel("Successfully imported!", f"Roadmap: {roadmap['title']}", True)

        except FileNotFoundError:
            print_panel("File not found!", "Please check the filename and path", False)
        except json.JSONDecodeError:
            print_panel("Invalid JSON file!", "The file is not a valid roadmap JSON", False)
        except Exception as e:
            print_panel(f"Import failed! Error: {str(e)}", "", False)

    console.print()
    console.print("[dim]Press Enter to continue...[/dim]", end="")
    input()