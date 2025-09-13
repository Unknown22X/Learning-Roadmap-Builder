import time
from data_manager import save_data
from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm

def manage_categories(data):
    """Main category management menu - allows viewing, adding, editing, and deleting categories"""
    console = Console()
    
    while True:
        # Clear screen and display main category management header
        console.clear()
        console.print(Panel.fit(
            "🗂️  [bold yellow]Manage Categories[/bold yellow]",
            subtitle="[dim]Organize your learning topics[/dim]",
            border_style="yellow",
            box=box.DOUBLE
        ))
        console.print()
        
        # Create and display menu options table
        options_table = Table(show_header=False, box=box.SIMPLE)
        options_table.add_row("1. [bold cyan]👀 View all categories[/bold cyan]")      # Option 1: View categories
        options_table.add_row("2. [bold green]➕ Add category[/bold green]")           # Option 2: Add new category
        options_table.add_row("3. [bold blue]✏️ Edit category[/bold blue]")           # Option 3: Edit existing category
        options_table.add_row("4. [bold red]🗑️ Delete category[/bold red]")           # Option 4: Delete category
        options_table.add_row("5. [dim]↩️ Back to main menu[/dim]")                   # Option 5: Return to main menu
        console.print(options_table)
        console.print()
        
        try:
            choice = Prompt.ask(
                "[bold]Select option[/bold]",
                choices=["1", "2", "3", "4", "5", "q"],
                show_choices=False
            )
            
            if choice == "5" or choice.lower() == "q":
                break
                
            if choice == "1":
                view_categories(data)      # Show all categories
            elif choice == "2":
                add_category(data)         # Add new category
            elif choice == "3":
                edit_category(data)        # Edit existing category
            elif choice == "4":
                delete_category(data)      # Delete category
                
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            break
        except:
            console.print("[red]❌ Invalid selection![/red]")
            time.sleep(1)

def view_categories(data):
    """Display all categories in a formatted table with usage statistics"""
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
        # Create table to display categories with their usage info
        cat_table = Table(title="📊 Category Overview", box=box.ROUNDED)
        cat_table.add_column("#", style="bold cyan", width=4, justify="center")        # Column 1: Category number
        cat_table.add_column("Category", style="bold white")                           # Column 2: Category name
        cat_table.add_column("Roadmaps", style="green", justify="center")              # Column 3: Number of roadmaps using this category
        cat_table.add_column("Status", style="dim", justify="center")                  # Column 4: Usage status (Used/Empty)
        
        # Populate table with category data
        for i, category in enumerate(data["categories"], start=1):
            # Count how many roadmaps use this category
            count = sum(1 for roadmap in data["roadmaps"] if roadmap.get("category") == category)
            status = "✅ Used" if count > 0 else "📭 Empty"  # Show status based on usage
            cat_table.add_row(str(i), category, str(count), status)
        
        console.print(cat_table)  
    
    console.print()
    Prompt.ask("[dim]Press Enter to continue...[/dim]", default="", show_default=False)

def add_category(data):
    """Add a new category to the system"""
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
        # Error: Empty category name
        console.print("[red]❌ Category name cannot be empty![/red]")
    elif new_category in data["categories"]:
        # Error: Category already exists
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
    """Edit an existing category name and update all roadmaps using it"""
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
            default=old_category  # Pre-fill with current name
        )
        
        if not new_category.strip():
            console.print("[red]❌ Category name cannot be empty![/red]")
        elif new_category != old_category and new_category in data["categories"]:
            console.print("[yellow]⚠️ Category already exists![/yellow]")
        else:
            # Update all roadmaps that use the old category name
            if new_category != old_category:
                for roadmap in data["roadmaps"]:
                    if roadmap.get("category") == old_category:
                        roadmap["category"] = new_category 
            
            # Update the category in the categories list
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
    """Delete a category after checking if it's used by any roadmaps"""
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
            # ADD THIS LINE TO PAUSE BEFORE RETURNING:
            Prompt.ask("[dim]Press Enter to continue...[/dim]", default="", show_default=False)
            return  # ← This return was already here
            
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