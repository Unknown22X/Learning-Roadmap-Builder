import json
import time
from data_manager import save_data
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
def import_export_roadmaps(data):
    console = Console()
    console.clear()
    
    # Beautiful header
    console.print(Panel.fit(
        "💾 [bold magenta]Import/Export Roadmaps[/bold magenta]",
        subtitle="[dim]Backup and share your learning journeys[/dim]",
        border_style="magenta",
        box=box.DOUBLE
    ))
    console.print()
    
    # Options table with quit option
    options_table = Table(show_header=False, box=box.SIMPLE)
    options_table.add_row("1. [bold green]📤 Export roadmap[/bold green]")
    options_table.add_row("2. [bold blue]📥 Import roadmap[/bold blue]")
    options_table.add_row("q. [dim]↩️  Back to main menu[/dim]")
    console.print(options_table)
    console.print()
    
    # Get choice with quit option
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
    except:
        console.print("[red]❌ Invalid selection![/red]")
        return
        
    if choice == 1:
        # Export roadmap
        if not data["roadmaps"]:
            console.print(Panel.fit(
                "[yellow]📭 No roadmaps to export[/yellow]",
                subtitle="[dim]Create roadmaps first to export them[/dim]",
                border_style="yellow",
                box=box.ROUNDED
            ))
            time.sleep(1.5)
            return
            
        # Display roadmaps table with quit option
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
        
        # Get roadmap selection with quit option
        try:
            idx_input = Prompt.ask(
                "[bold]Select roadmap number (or 'q' to quit)[/bold]",
                choices=[str(i) for i in range(1, len(data["roadmaps"]) + 1)] + ["q", "Q"],
                show_choices=False
            )
            if idx_input.lower() == 'q':
                console.print("[dim]Export cancelled.[/dim]")
                return
            idx = int(idx_input) - 1
        except:
            console.print("[red]❌ Invalid selection![/red]")
            return     
            
        # Get filename with quit option
        filename = Prompt.ask("[bold]Enter export filename (or 'q' to quit)[/bold]", default="roadmap.json")
        if filename.lower() == 'q':
            console.print("[dim]Export cancelled.[/dim]")
            return
        if not filename.endswith('.json'):
            filename += '.json'
            
        # Export
        try:
            with console.status("[bold green]Exporting roadmap...[/]"):
                with open(filename, "w") as f:
                    json.dump(data["roadmaps"][idx], f, indent=4)
                time.sleep(0.5)
                
            console.print()
            console.print(Panel.fit(
                f"✅ [bold green]Successfully exported![/bold green]",
                subtitle=f"[dim]File: {filename}[/dim]",
                border_style="bright_green",
                box=box.ROUNDED
            ))
            
        except IOError as e:
            console.print(Panel.fit(
                f"❌ [red]Export failed![/red]",
                subtitle=f"[dim]Error: {str(e)}[/dim]",
                border_style="red",
                box=box.ROUNDED
            ))
            
    else:
        # Import roadmap with quit option
        filename = Prompt.ask("[bold]Enter import filename (or 'q' to quit)[/bold]")
        if filename.lower() == 'q':
            console.print("[dim]Import cancelled.[/dim]")
            return
        
        try:
            with console.status("[bold blue]Importing roadmap...[/]"):
                with open(filename, "r") as f:
                    roadmap = json.load(f)
                time.sleep(0.5)
                
            # Add to data and save
            data["roadmaps"].append(roadmap)
            save_data(data)
            
            console.print()
            console.print(Panel.fit(
                f"✅ [bold green]Successfully imported![/bold green]",
                subtitle=f"[dim]Roadmap: {roadmap['title']}[/dim]",
                border_style="bright_green",
                box=box.ROUNDED
            ))
            
        except FileNotFoundError:
            console.print(Panel.fit(
                "❌ [red]File not found![/red]",
                subtitle="[dim]Please check the filename and path[/dim]",
                border_style="red",
                box=box.ROUNDED
            ))
        except json.JSONDecodeError:
            console.print(Panel.fit(
                "❌ [red]Invalid JSON file![/red]",
                subtitle="[dim]The file is not a valid roadmap JSON[/dim]",
                border_style="red",
                box=box.ROUNDED
            ))
        except Exception as e:
            console.print(Panel.fit(
                f"❌ [red]Import failed![/red]",
                subtitle=f"[dim]Error: {str(e)}[/dim]",
                border_style="red",
                box=box.ROUNDED
            ))
    
    # Pause before returning to menu
    console.print()
    console.print("[dim]Press Enter to continue...[/dim]", end="")
    input()