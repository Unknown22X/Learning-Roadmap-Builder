import time
from data_manager import save_data
from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm

def manage_categories(data):
    """Main menu for category management."""
    console = Console()
    
    while True:
        console.clear()
        console.print(Panel.fit(
            "🗂️  [bold yellow]Manage Categories[/bold yellow]",
            subtitle="[dim]Organize your learning topics[/dim]",
            border_style="yellow",
            box=box.DOUBLE
        ))
        console.print()
        
        options_table = Table(show_header=False, box=box.SIMPLE)
        options_table.add_row("1. [bold cyan]👀 View all categories[/bold cyan]")
        options_table.add_row("2. [bold green]➕ Add category[/bold green]")
        options_table.add_row("3. [bold blue]✏️ Edit category[/bold blue]")
        options_table.add_row("4. [bold red]🗑️ Delete category[/bold red]")
        options_table.add_row("5. [dim]↩️ Back to main menu[/dim]")
        console.print(options_table)
        console.print()
        
        try:
            choice = Prompt.ask(
                "[bold]Select option[/bold]",
                choices=["1", "2", "3", "4", "5", "q"],
                show_choices=False
            )
            
            if choice in ("5", "q"):
                break
                
            if choice == "1":
                view_categories(data)
            elif choice == "2":
                add_category(data)
            elif choice == "3":
                edit_category(data)
            elif choice == "4":
                delete_category(data)
                
        except KeyboardInterrupt:
            break
        except:
            console.print("[red]❌ Invalid selection![/red]")
            time.sleep(1)

def view_categories(data):
    """Displays all categories and their usage count."""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "👀 [bold cyan]All Categories[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED
    ))
    console.print()
    
    if not data["categories"]:
        console.print(Panel.fit(
            "[yellow]📭 No categories found[/yellow]",
            border_style="yellow",
            box=box.ROUNDED
        ))
    else:
        cat_table = Table(title="📊 Category Overview", box=box.ROUNDED)
        cat_table.add_column("#", style="bold cyan", width=4, justify="center")
        cat_table.add_column("Category", style="bold white")
        cat_table.add_column("Roadmaps", style="green", justify="center")
        cat_table.add_column("Status", style="dim", justify="center")
        
        for i, category in enumerate(data["categories"], start=1):
            count = sum(1 for roadmap in data["roadmaps"] if roadmap.get("category") == category)
            status = "✅ Used" if count > 0 else "📭 Empty"
            cat_table.add_row(str(i), category, str(count), status)
        
        console.print(cat_table)  
    
    console.print()
    Prompt.ask("[dim]Press Enter to continue...[/dim]", default="", show_default=False)

def add_category(data):
    """Adds a new category."""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "➕ [bold green]Add New Category[/bold green]",
        border_style="green",
        box=box.ROUNDED
    ))
    console.print()
    
    new_category = Prompt.ask("[bold]Enter new category name[/bold]")
    
    if not new_category.strip():
        console.print("[red]❌ Category name cannot be empty![/red]")
    elif new_category in data["categories"]:
        console.print("[yellow]⚠️ Category already exists![/yellow]")
    else:
        data["categories"].append(new_category)
        save_data(data)
        console.print(Panel.fit(
            f"✅ [bold green]Category '{new_category}' added![/bold green]",
            border_style="bright_green",
            box=box.ROUNDED
        ))
    
    console.print()
    Prompt.ask("[dim]Press Enter to continue...[/dim]", default="", show_default=False)

def edit_category(data):
    """Edits an existing category."""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "✏️  [bold blue]Edit Category[/bold blue]",
        border_style="blue",
        box=box.ROUNDED
    ))
    console.print()
    
    if not data["categories"]:
        console.print(Panel.fit(
            "[yellow]📭 No categories to edit[/yellow]",
            border_style="yellow",
            box=box.ROUNDED
        ))
        console.print()
        Prompt.ask("[dim]Press Enter to continue...[/dim]", default="", show_default=False)
        return
    
    view_categories(data)
    console.print()
    
    try:
        choice = IntPrompt.ask(
            "[bold]Enter category number to edit (or 0 to cancel)[/bold]",
            choices=[str(i) for i in range(0, len(data["categories"]) + 1)],
            show_choices=False
        )
        
        if choice == 0:
            console.print("[dim]Edit cancelled.[/dim]")
            return
            
        old_category = data["categories"][choice - 1]
        
        console.print()
        new_category = Prompt.ask(
            f"[bold]Enter new name for '{old_category}'[/bold]",
            default=old_category
        )
        
        if not new_category.strip():
            console.print("[red]❌ Category name cannot be empty![/red]")
        elif new_category != old_category and new_category in data["categories"]:
            console.print("[yellow]⚠️ Category already exists![/yellow]")
        else:
            if new_category != old_category:
                for roadmap in data["roadmaps"]:
                    if roadmap.get("category") == old_category:
                        roadmap["category"] = new_category 
            
            data["categories"][choice - 1] = new_category
            save_data(data)  
            
            console.print(Panel.fit(
                f"✅ [bold green]Category updated![/bold green]",
                subtitle=f"[dim]From '{old_category}' to '{new_category}'[/dim]",
                border_style="bright_green",
                box=box.ROUNDED
            ))
            
    except:
        console.print("[red]❌ Invalid selection![/red]")
    
    console.print()
    Prompt.ask("[dim]Press Enter to continue...[/dim]", default="", show_default=False)

def delete_category(data):
    """Deletes an unused category."""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "🗑️  [bold red]Delete Category[/bold red]",
        border_style="red",
        box=box.ROUNDED
    ))
    console.print()
    
    if not data["categories"]:
        console.print(Panel.fit(
            "[yellow]📭 No categories to delete[/yellow]",
            border_style="yellow",
            box=box.ROUNDED
        ))
        console.print()
        Prompt.ask("[dim]Press Enter to continue...[/dim]", default="", show_default=False)
        return
    
    view_categories(data)
    console.print()
    
    try:
        choice = IntPrompt.ask(
            "[bold]Enter category number to delete (or 0 to cancel)[/bold]",
            choices=[str(i) for i in range(0, len(data["categories"]) + 1)],
            show_choices=False
        )
        
        if choice == 0:
            console.print("[dim]Deletion cancelled.[/dim]")
            return
            
        category = data["categories"][choice - 1]
        
        used_by = [r for r in data["roadmaps"] if r.get("category") == category]
        if used_by:
            console.print(Panel.fit(
                f"❌ [red]Cannot delete '{category}'[/red]",
                subtitle=f"[dim]Used by {len(used_by)} roadmap(s)[/dim]",
                border_style="red",
                box=box.ROUNDED
            ))
            Prompt.ask("[dim]Press Enter to continue...[/dim]", default="", show_default=False)
            return
            
        if Confirm.ask(f"[bold red]Are you sure you want to delete '{category}'?[/bold red]"):
            data["categories"].pop(choice - 1)
            save_data(data)
            console.print(Panel.fit(
                f"✅ [bold green]Category '{category}' deleted![/bold green]",
                border_style="bright_green",
                box=box.ROUNDED
            ))
        else:
            console.print("[dim]Deletion cancelled.[/dim]")
            
    except:
        console.print("[red]❌ Invalid selection![/red]")
    
    console.print()
    Prompt.ask("[dim]Press Enter to continue...[/dim]", default="", show_default=False)