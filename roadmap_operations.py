from data_manager import save_data
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm, PromptError
from rich import box
from rich.table import Table
from config import MOTIVATIONAL_TIPS, ANIMATION_DELAY, PRIORITY_ORDER
import time

def create_roadmap(data):
    """Create a new learning roadmap with safe dictionary access"""
    console = Console()
    console.clear()
    console.print(Panel.fit("✨ [bold green]Create New Roadmap[/bold green]", 
                           subtitle="[dim]Start your learning journey[/]", 
                           border_style="green", box=box.DOUBLE))
    console.print()
    
    # Safe access to categories with default empty list
    categories = data.get("categories", [])
    
    categories_table = Table(show_header=False, box=box.SIMPLE)
    categories_table.add_column("#", style="bold cyan", width=4)
    categories_table.add_column('Category', style="white")
    
    # Show available categories
    console.print("[bold]Available categories:[/bold]")
    for i, category in enumerate(categories, start=1):
        categories_table.add_row(str(i), f"📂 {category}")
    console.print(categories_table)
    console.print(f"[dim]{len(categories) + 1}. Add new category[/dim]")
    console.print()
    
    # Get category choice
    try:
        cat_choice = IntPrompt.ask(
            "[yellow][bold]Select category number[/bold][/]",
            choices=[str(i) for i in range(1, len(categories) + 2)],
            show_choices=False
        )
    except PromptError:
        console.print("[red]Invalid selection! Please choose a valid category number.[/red]")
        return
    
    # Handle category selection
    if cat_choice == len(categories) + 1:
        # Add new category
        new_category = Prompt.ask("[bold]Enter new category name[/bold]")
        if new_category:
            # Ensure categories list exists in data
            if "categories" not in data:
                data["categories"] = []
            data["categories"].append(new_category)
            category = new_category
            console.print(f"[green]✅ Category '{new_category}' added.[/]")
        else:
            category = "Other"
            console.print("[yellow]Using 'Other' category[/yellow]")
    else:
        category = categories[cat_choice - 1]
        console.print(f"[cyan]Selected: 📂 {category}[/cyan]")
    
    # Get roadmap title
    title = Prompt.ask("[bold]Enter roadmap title[/bold]")
    if not title or title.isspace():
        console.print("[red]❌ Title cannot be empty or just spaces.[/]")
        return
    
    if title:
        # Ensure roadmaps list exists in data
        if "roadmaps" not in data:
            data["roadmaps"] = []
        
        data["roadmaps"].append({
            "title": title, 
            "category": category,
            "steps": []  # Always initialize with empty steps list
        })
        save_data(data)
        
    console.print(Panel.fit(
        f"✅ [bold green]Roadmap '{title}' created![/bold green]",
        subtitle=f"[dim]Category: {category}[/dim]",
        border_style="bright_green",
        box=box.ROUNDED
    ))

def add_step(data):
    """Add a step to an existing roadmap with safe dictionary access"""
    console = Console()
    console.print(Panel.fit("[bold green]➕ Add Step[/bold green]", 
                           border_style="green", box=box.DOUBLE))
    
    # Safe access to roadmaps with default empty list
    roadmaps = data.get("roadmaps", [])
    
    if not roadmaps:
        console.print("[yellow][bold]No roadmaps available.[/bold][/]")
        console.print("[dim][yellow]Try option 2 to create a roadmap[/][/]")
        return
    
    table = Table(title="🗺️   Select Roadmap", box=box.ROUNDED)
    table.add_column("#", style="bold cyan", width=4, justify="center")
    table.add_column("Title", style="bold orchid")
    
    for i, roadmap in enumerate(roadmaps, start=1):
        # Safe access to roadmap title with default
        title = roadmap.get("title", "Untitled")
        table.add_row(str(i), title)
    
    console.print(table)
    console.print()

    while True:
        val = Prompt.ask("[bold cyan]Enter roadmap number (or 'q' to quit)[/]", show_choices=False)
        if val == "q":
            return
        try:
            idx = int(val) - 1
            if idx < 0 or idx >= len(roadmaps):
                console.print("[red]Invalid selection.[/red]")
            else:
                break
        except ValueError:
            console.print("[red]Please enter a number or 'q' to quit.[/red]")

    console.print()
    step_title = Prompt.ask("[bold]Enter step title[/bold]").strip()
    if not step_title:
        console.print("[red]❌ Step title cannot be empty.[/red]")
        return
    
    try:
        priority_choice = IntPrompt.ask("[bold]Priority : 1 ~ high , 2 ~ medium , 3 ~ low, 4 ~ none[/bold]", 
                                      choices=["1", "2", "3", "4"])
        priority_map = {1: "high", 2: "medium", 3: "low", 4: "none"}
        priority = priority_map[priority_choice]
    except:
        priority = "none"
    
    # Ensure the selected roadmap has a steps list
    if "steps" not in roadmaps[idx]:
        roadmaps[idx]["steps"] = []
    
    roadmaps[idx]["steps"].append({
        "title": step_title, 
        "done": False, 
        "priority": priority
    })
    
    with console.status("[bold green]Saving...[/]"):
        save_data(data)
        time.sleep(0.5)
    
    # Safe access to roadmap title for confirmation message
    roadmap_title = roadmaps[idx].get("title", "Untitled")
    console.print(Panel.fit(
        f"✅ [bold green]Step '{step_title}' added to '{roadmap_title}'.[/]",
        border_style="bright_green",
        box=box.ROUNDED
    ))

def mark_step_complete(data):
    """Mark a step as complete/incomplete with safe dictionary access"""
    console = Console()
    console.clear()
    console.print(Panel.fit("✨ [bold green]Mark step complete[/bold green]", 
                           border_style="pale_green1", box=box.DOUBLE))
    
    # Safe access to roadmaps with default empty list
    roadmaps = data.get("roadmaps", [])
    
    if not roadmaps:
        console.print("[red]❌ No roadmaps available[/]")
        return
    
    table = Table(title="🗺️   Select Roadmap", box=box.ROUNDED)
    table.add_column("#", style="bold plum2", width=4, justify="center")
    table.add_column("Title", style="bold grey82")

    for i, roadmap in enumerate(roadmaps, start=1):
        # Safe access to roadmap title with default
        title = roadmap.get("title", "Untitled")
        table.add_row(str(i), title)
    
    console.print(table)
    console.print()
    
    while True:
        val = Prompt.ask("[bold cyan]Enter roadmap number (or 'q' to quit)[/]", show_choices=False)
        if val == "q":
            return
        try:
            idx = int(val) - 1
            if idx < 0 or idx >= len(roadmaps):
                console.print("[red]Invalid selection.[/red]")
            else:
                break
        except ValueError:
            console.print("[red]Please enter a number or 'q' to quit.[/red]")

    # Safe access to steps with default empty list
    steps = roadmaps[idx].get("steps", [])
    
    if not steps:
        console.print("[bold yellow]This roadmap has no steps yet.[/]")
        return
    
    table = Table(title="🗺️   Select a step", box=box.ROUNDED)
    table.add_column("#", style="bold light_steel_blue", width=4, justify="center")
    table.add_column("Title", style="bold hot_pink3")

    for i, step in enumerate(steps, start=1):
        # Safe access to step title with default
        step_title = step.get("title", "Untitled Step")
        table.add_row(str(i), step_title)
    
    console.print(table)
    console.print()
    
    while True:
        val = Prompt.ask("[bold cyan]Enter step number (or 'q' to quit)[/]", show_choices=False)
        if val == "q":
            return
        try:
            idxs = int(val) - 1
            if idxs < 0 or idxs >= len(steps):
                console.print("[red]Invalid selection.[/red]")
            else:
                break
        except ValueError:
            console.print("[red]Please enter a number or 'q' to quit.[/red]")
    
    # Safe access to step done status with default False
    current_status = steps[idxs].get("done", False)
    steps[idxs]["done"] = not current_status
    state = "complete" if steps[idxs]["done"] else "incomplete"
    
    with console.status("[bold green]Saving...[/]"):
        save_data(data)
        time.sleep(0.5)
    
    # Safe access to step title for confirmation
    step_title = steps[idxs].get("title", "Untitled Step")
    console.print(Panel.fit(
        f"✅ [bold green]Step '{step_title}' marked as {state}.[/]",
        border_style="bright_green",
        box=box.ROUNDED
    ))

def get_highest_priority_score(roadmap):
    """Get numerical score for roadmap's highest priority step with safe access"""
    # Safe access to steps with default empty list
    steps = roadmap.get("steps", [])
    
    if not steps:
        return 3  # Default priority score when no steps exist
    
    return min(
        PRIORITY_ORDER.get(step.get("priority", "none"), 3)
        for step in steps
    )

def sort_by_priority(items, is_roadmap=False):
    """
    Sort by priority - works for both steps and roadmaps with safe access
    items: either list of steps or list of roadmaps
    is_roadmap: True if sorting roadmaps, False if sorting steps
    """
    if is_roadmap:
        # Sort roadmaps by their highest priority step
        return sorted(items, key=lambda roadmap: get_highest_priority_score(roadmap))
    else:
        # Sort steps within a roadmap - safe access to priority
        return sorted(items, key=lambda step: PRIORITY_ORDER.get(step.get("priority", "none"), 3))

def sort_roadmaps(data):
    """Sort roadmaps by various criteria with safe dictionary access"""
    console = Console()
    console.print(Panel.fit("[red]🗃️  Sort Roadmaps[/]", border_style="red", box=box.DOUBLE))
    
    # Safe access to roadmaps with default empty list
    roadmaps = data.get("roadmaps", [])
    
    if not roadmaps:
        console.print("[red]No roadmaps to sort.[/]")
        return
 
    table = Table()
    table.add_column("#")
    table.add_column("Option")
    table.add_row("1", "Sort by title")
    table.add_row("2", "Sort by progress") 
    table.add_row("3", "Sort by category")
    table.add_row("4", "Sort by priority")
    console.print(table)
    
    try:
        choice = IntPrompt.ask(
            "[yellow][bold]Select option[/bold][/yellow]",
            choices=["1", "2", "3", "4"],
            show_choices=False
        )
    except:
        console.print("[red]❌ Invalid selection![/red]")
        return

    if choice == 1:
        # Sort by title - safe access with default
        roadmaps.sort(key=lambda x: x.get("title", "Untitled").lower())
    elif choice == 2:
        # Sort by progress - safe access to steps and done status
        def get_progress(roadmap):
            steps = roadmap.get("steps", [])
            if not steps:
                return 0
            completed_count = sum(1 for step in steps if step.get("done", False))
            return completed_count / len(steps)
        
        roadmaps.sort(key=get_progress, reverse=True)
    elif choice == 3:
        # Sort by category - safe access with default
        roadmaps.sort(key=lambda x: x.get("category", "Uncategorized"))
    elif choice == 4: 
        # Sort roadmaps by priority
        data["roadmaps"] = sort_by_priority(roadmaps, is_roadmap=True)
        
        # Sort steps within each roadmap by priority
        for roadmap in roadmaps:
            steps = roadmap.get("steps", [])
            if steps:
                roadmap["steps"] = sort_by_priority(steps, is_roadmap=False)
    
    with console.status("[bold green]Saving...[/]"):
        save_data(data)
        time.sleep(0.5)
    
    console.print(Panel.fit(
        f"✅ [bold green]Roadmaps have been sorted.[/]",
        border_style="bright_green", 
        box=box.ROUNDED
    ))

def edit_roadmap(data):
    """Edit roadmap or step titles with safe dictionary access"""
    console = Console()
    console.clear()
    
    # Beautiful header
    console.print(Panel.fit(
        "✏️  [bold cyan]Edit Roadmap/Step[/bold cyan]",
        subtitle="[dim]Modify your learning content[/dim]",
        border_style="cyan",
        box=box.DOUBLE
    ))
    console.print()
    
    # Safe access to roadmaps with default empty list
    roadmaps = data.get("roadmaps", [])
    
    if not roadmaps:
        console.print(Panel.fit(
            "[yellow]📭 No roadmaps available[/yellow]",
            subtitle="[dim]Create a roadmap first to edit content[/dim]",
            border_style="yellow",
            box=box.ROUNDED
        ))
        return

    # Display roadmaps in a table
    roadmap_table = Table(title="🗺️       Select Roadmap to Edit", box=box.ROUNDED)
    roadmap_table.add_column("#", style="bold cyan", width=4, justify="center")
    roadmap_table.add_column("Roadmap", style="bold white")
    roadmap_table.add_column("Category", style="dim", justify="center")
    roadmap_table.add_column("Steps", style="green", justify="center")
    
    for i, roadmap in enumerate(roadmaps, start=1):
        # Safe access to roadmap properties with defaults
        title = roadmap.get("title", "Untitled")
        category = roadmap.get("category", "Uncategorized")
        steps = roadmap.get("steps", [])
        steps_count = len(steps)
        
        roadmap_table.add_row(str(i), title, category, str(steps_count))
    
    console.print(roadmap_table)
    console.print()

    # Get roadmap selection
    try:
        roadmap_num = IntPrompt.ask(
            "[bold]Select roadmap number[/bold]",
            choices=[str(i) for i in range(1, len(roadmaps) + 1)],
            show_choices=False
        )
    except:
        console.print("[red]❌ Operation cancelled[/red]")
        return
    
    roadmap_idx = roadmap_num - 1

    # Edit options
    console.print()
    console.print(Panel.fit(
        "⚙️  [bold]Edit Options[/bold]",
        border_style="bright_blue",
        box=box.SIMPLE
    ))
    
    option_table = Table(show_header=False, box=None)
    option_table.add_row("1. [bold green]Edit roadmap title[/bold green]")
    option_table.add_row("2. [bold blue]Edit step title[/bold blue]")
    console.print(option_table)
    console.print()

    try:
        option = IntPrompt.ask(
            "[bold]Select option[/bold]",
            choices=["1", "2"],
            show_choices=False
        )
    except:
        console.print("[red]❌ Invalid option[/red]")
        return

    if option == 1:
        # Edit roadmap title
        new_title = Prompt.ask("[bold]Enter new roadmap title[/bold]")
        if not new_title.strip():
            console.print("[red]❌ Title cannot be empty![/red]")
            return
            
        # Safe access to current title with default
        old_title = roadmaps[roadmap_idx].get("title", "Untitled")
        roadmaps[roadmap_idx]["title"] = new_title.strip()
        
        with console.status("[bold green]Saving changes...[/]"):
            save_data(data)
            time.sleep(0.5)
        
        console.print()
        console.print(Panel.fit(
            f"✅ [bold green]Title updated![/bold green]",
            subtitle=f"[dim]From '{old_title}' to '{new_title}'[/dim]",
            border_style="bright_green",
            box=box.ROUNDED
        ))
        
    else:
        # Edit step title
        # Safe access to steps with default empty list
        steps = roadmaps[roadmap_idx].get("steps", [])
        
        if not steps:
            console.print(Panel.fit(
                "[yellow]📝 No steps available[/yellow]",
                subtitle="[dim]Add steps first to edit them[/dim]",
                border_style="yellow",
                box=box.ROUNDED
            ))
            return

        # Display steps table
        steps_table = Table(title="📋 Select Step to Edit", box=box.ROUNDED)
        steps_table.add_column("#", style="bold cyan", width=4, justify="center")
        steps_table.add_column("Current Title", style="bold white")
        steps_table.add_column("Status", style="green", justify="center")
        
        for i, step in enumerate(steps, start=1):
            # Safe access to step properties with defaults
            step_title = step.get("title", "Untitled Step")
            is_done = step.get("done", False)
            status = "✅ Done" if is_done else "⏳ Pending"
            steps_table.add_row(str(i), step_title, status)
        
        console.print(steps_table)
        console.print()

        try:
            step_num = IntPrompt.ask(
                "[bold]Select step number[/bold]",
                choices=[str(i) for i in range(1, len(steps) + 1)],
                show_choices=False
            )
        except:
            console.print("[red]❌ Invalid selection[/red]")
            return
            
        step_idx = step_num - 1
        
        # Get new step title
        new_step_title = Prompt.ask("[bold]Enter new step title[/bold]")
        if not new_step_title.strip():
            console.print("[red]❌ Step title cannot be empty![/red]")
            return
            
        # Safe access to current step title with default
        old_step_title = steps[step_idx].get("title", "Untitled Step")
        steps[step_idx]["title"] = new_step_title.strip()
        
        with console.status("[bold green]Saving changes...[/]"):
            save_data(data)
            time.sleep(0.5)
        
        console.print()
        console.print(Panel.fit(
            f"✅ [bold green]Step updated![/bold green]",
            subtitle=f"[dim]From '{old_step_title}' to '{new_step_title}'[/dim]",
            border_style="bright_green",
            box=box.ROUNDED
        ))

def delete_roadmap_or_step(data):
    """Delete roadmap or step with safe dictionary access"""
    console = Console()
    console.print(Panel.fit("[red]🗑️  Delete Roadmap/Step[/]", 
                           border_style="red", box=box.DOUBLE))
    
    try:
        oper = IntPrompt.ask(
            "[yellow][bold]Enter 1 to delete a roadmap, 2 to delete a step[/][/]",
            choices=["1", "2"],
            show_choices=False
        )
    except:
        console.print("[red]Invalid selection![/red]")
        return
         
    # Safe access to roadmaps with default empty list
    roadmaps = data.get("roadmaps", [])
    
    if not roadmaps:
        console.print("[yellow][bold]No roadmaps available.[/bold][/]")
        console.print("[dim][yellow]Press 2 to create a roadmap first[/][/] ")
        return
    
    roadmap_table = Table(title="🗺️  Select roadmap", box=box.ROUNDED)
    roadmap_table.add_column("#", style="bold cyan", width=4, justify="center")
    roadmap_table.add_column("Roadmap", style="bold orchid", justify='center')
    
    for i, roadmap in enumerate(roadmaps, start=1):
        # Safe access to roadmap title with default
        title = roadmap.get('title', 'Untitled')
        roadmap_table.add_row(str(i), title)
    
    console.print(roadmap_table)
    console.print()

    try:
        roadmap_idx = IntPrompt.ask(
            "[red][bold]Select Roadmap number[/bold][/]",
            choices=[str(i) for i in range(1, len(roadmaps) + 1)],
            show_choices=False
        )
        roadmap_idx = roadmap_idx - 1 
    except:
        console.print("[red]Invalid selection![/red]")
        return

    if oper == 1:  
        # Delete entire roadmap
        # Safe access to roadmap title for confirmation
        roadmap_title = roadmaps[roadmap_idx].get('title', 'Untitled')
        
        try: 
            confirm = Prompt.ask(
                f"[bold][yellow]⚠️   Are you sure you want to delete '{roadmap_title}'? (y/n): [/][/]", 
                choices=["y", "n"], 
                show_choices=False, 
                case_sensitive=False
            )
        except:
            console.print("[red]Invalid selection![/red]")
            return
            
        if confirm.lower() != "y":
            console.print("[green]Deletion canceled.[/green]")
            return
            
        deleted = roadmaps.pop(roadmap_idx)
        save_data(data)
        deleted_title = deleted.get('title', 'Untitled')
        console.print(Panel.fit(
            f"✅ [bold green]Roadmap '{deleted_title}' deleted.[/]", 
            border_style="bright_green", 
            box=box.ROUNDED
        ))

    elif oper == 2:
        # Delete step from roadmap
        # Safe access to steps with default empty list
        steps = roadmaps[roadmap_idx].get("steps", [])
        
        if not steps:
            console.print("[bold yellow]This roadmap has no steps yet.[/]")
            return
       
        steps_table = Table(title="🗺️ Select a step", box=box.ROUNDED)
        steps_table.add_column("#", style="bold cyan", width=4, justify="center")  
        steps_table.add_column("Title", style="bold violet")
        console.print()
        
        for i, step in enumerate(steps, start=1): 
            # Safe access to step title with default
            step_title = step.get("title", "Untitled Step")
            steps_table.add_row(str(i), step_title)
        
        console.print(steps_table)
        
        try:
            step_num = IntPrompt.ask(
                f"[bold cyan]Enter a step number[/]",
                choices=[str(i) for i in range(1, len(steps) + 1)], 
                show_choices=False
            )
            console.print()
        except:
            console.print("[red]❌ Invalid input. Please enter a valid number.[/]")
            return
            
        step_idx = int(step_num) - 1
        
        # Safe access to step title for confirmation
        step_title = steps[step_idx].get('title', 'Untitled Step')
        
        confirm = Confirm.ask(f"Are you sure you want to delete '{step_title}'?", console=console)
        if confirm:
            deleted = steps.pop(step_idx)
            with console.status("[bold green]Saving...[/]"):
                save_data(data)
                time.sleep(0.5)
            
            deleted_title = deleted.get('title', 'Untitled Step')
            roadmap_title = roadmaps[roadmap_idx].get('title', 'Untitled')
            console.print(f"[bold green]Step '{deleted_title}' deleted from roadmap '{roadmap_title}'.[/]")
        else: 
            console.print(f"[bold red]Deletion canceled.[/]")
            return

def search(data):
    """Search roadmaps by title, category or step content with safe dictionary access"""
    console = Console()
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]🔍 Search Roadmaps & Steps[/]",
        subtitle="Find your learning content", 
        border_style="cyan", 
        box=box.DOUBLE
    ))
    console.print()
    
    # Safe access to roadmaps with default empty list
    roadmaps = data.get("roadmaps", [])
    
    if not roadmaps:
        console.print("[bold red]No roadmaps available.[/]")
        console.print("[dim][yellow]Try option 2 to create a roadmap[/][/]")
        return
    
    try:
        keyword = Prompt.ask("🔍 Enter search keyword").strip().lower()
        if not keyword:
            console.print("[red]Search keyword cannot be empty[/]")
            return
    except PromptError: 
        console.print("[red]Invalid input! Please enter a valid keyword.[/red]")
        return
    
    # Collect matches
    roadmaps_results = []
    steps_results = []
    
    for roadmap in roadmaps:
        # Safe access to roadmap properties with defaults
        title = roadmap.get("title", "Untitled")
        category = roadmap.get("category", "")
        steps = roadmap.get("steps", [])
        
        match_reasons = []
        
        # Check if keyword matches roadmap title
        if keyword in title.lower():
            match_reasons.append("Title")
            
        # Check if keyword matches category
        if keyword in category.lower():
            match_reasons.append("Category")
        
        # Search in steps
        match_steps = []
        for step in steps:
            # Safe access to step title with default
            step_title = step.get("title", "Untitled Step")
            if keyword in step_title.lower():
                match_steps.append(step)
        
        if match_steps:
            match_reasons.append("Steps")
            steps_results.extend([(roadmap, step) for step in match_steps])
        
        if match_reasons:
            roadmaps_results.append((roadmap, ", ".join(match_reasons)))
    
    # Display results 
    if not roadmaps_results and not steps_results:
        console.print(f"[red]No matches found for '{keyword}'.[/red]")
        return        
    
    if roadmaps_results: 
        console.print(f"\n[cyan bold]Found {len(roadmaps_results)} roadmap(s) matching '{keyword}'[/]")
        table = Table(title="🗺️   Roadmap Search Results", box=box.ROUNDED, style="red")  
        table.add_column("#", style="bold cyan", width=4, justify="center") 
        table.add_column("Title", style="bold orchid")
        table.add_column("Category", style="white")
        table.add_column("Progress", style="green", justify="center")
        table.add_column("Matched On", style="yellow")
        
        for i, (roadmap, reasons) in enumerate(roadmaps_results, start=1):
            # Safe access to roadmap properties for display
            title = roadmap.get("title", "Untitled")
            category = roadmap.get("category", "Uncategorized")
            steps = roadmap.get("steps", [])
            
            # Calculate progress safely
            completed = sum(1 for step in steps if step.get("done", False))
            percent = (completed / len(steps)) * 100 if len(steps) > 0 else 0
            
            table.add_row(str(i), title, category, f"{percent:.1f}%", reasons)
        console.print(table)
    
    if steps_results: 
        console.print(f"\n[bold cyan]Found {len(steps_results)} step(s) matching '{keyword}'[/bold cyan]")
        table = Table(title="📝 Step Search Results", box=box.ROUNDED)
        table.add_column("#", style="bold cyan", width=4, justify="center")
        table.add_column("Step Title", style="bold violet")
        table.add_column("Roadmap", style="white")
        table.add_column("Status", style="green")
        
        for i, (roadmap, step) in enumerate(steps_results, start=1):
            # Safe access to step and roadmap properties
            step_title = step.get("title", "Untitled Step")
            roadmap_title = roadmap.get("title", "Untitled")
            is_done = step.get("done", False)
            status = "✅ Done" if is_done else "❌ Not Done"
            table.add_row(str(i), step_title, roadmap_title, status)
        console.print(table)

def show_help():
    """Display help and support information"""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "❓ [bold yellow]Help & Support[/bold yellow]",
        border_style="yellow",
        box=box.ROUNDED
    ))
    console.print()
    
    help_table = Table(show_header=False, box=None)
    help_table.add_row("💡 [bold]Need help?[/bold]", "Check the documentation")
    help_table.add_row("🐛 [bold]Found a bug?[/bold]", "Report it on GitHub")
    help_table.add_row("💡 [bold]Have ideas?[/bold]", "Suggest new features!")
    console.print(help_table)
    
    console.print()
    console.print(Panel.fit(
        "👨‍💻 [bold]Contact the Developer:[/bold]\n"
        "• [blue]GitHub: https://github.com/Unknown22X[/blue]\n"
        "• [green]Telegram: WE_CX [/green]\n",
        border_style="bright_blue",
        box=box.ROUNDED
    ))

# Additional helper functions for safe data handling

def validate_data_structure(data):
    """
    Validate and fix data structure to ensure required keys exist
    This function can be called at startup to ensure data integrity
    """
    # Ensure main data structure exists
    if not isinstance(data, dict):
        data = {}
    
    # Ensure categories list exists with .get() for safety
    if "categories" not in data:
        data["categories"] = []
    
    # Ensure roadmaps list exists with .get() for safety  
    if "roadmaps" not in data:
        data["roadmaps"] = []
    
    # Validate each roadmap structure
    for roadmap in data.get("roadmaps", []):
        # Ensure each roadmap has required fields
        if "title" not in roadmap:
            roadmap["title"] = "Untitled"
        if "category" not in roadmap:
            roadmap["category"] = "Uncategorized"
        if "steps" not in roadmap:
            roadmap["steps"] = []
            
        # Validate each step structure
        for step in roadmap.get("steps", []):
            if "title" not in step:
                step["title"] = "Untitled Step"
            if "done" not in step:
                step["done"] = False
            if "priority" not in step:
                step["priority"] = "none"
    
    return data

def get_roadmap_stats(roadmap):
    """
    Get statistics for a roadmap with safe dictionary access
    Returns: dict with total_steps, completed_steps, progress_percent
    """
    # Safe access to steps with default empty list
    steps = roadmap.get("steps", [])
    total_steps = len(steps)
    
    if total_steps == 0:
        return {
            "total_steps": 0,
            "completed_steps": 0,
            "progress_percent": 0.0
        }
    
    # Count completed steps safely
    completed_steps = sum(1 for step in steps if step.get("done", False))
    progress_percent = (completed_steps / total_steps) * 100
    
    return {
        "total_steps": total_steps,
        "completed_steps": completed_steps, 
        "progress_percent": progress_percent
    }

def get_priority_color(priority):
    """
    Get color for priority level with safe access
    Returns appropriate color string for rich console
    """
    # Safe access to priority with default "none"
    priority = str(priority).lower() if priority else "none"
    
    color_map = {
        "high": "red",
        "medium": "yellow", 
        "low": "blue",
        "none": "dim"
    }
    
    return color_map.get(priority, "dim")

def format_step_display(step, include_priority=True):
    """
    Format a step for display with safe dictionary access
    Returns formatted string for console output
    """
    # Safe access to step properties with defaults
    title = step.get("title", "Untitled Step")
    done = step.get("done", False)
    priority = step.get("priority", "none")
    
    # Status indicator
    status_icon = "✅" if done else "❌"
    
    if include_priority and priority != "none":
        priority_color = get_priority_color(priority)
        return f"{status_icon} [{priority_color}]{priority.upper()}[/{priority_color}] {title}"
    else:
        return f"{status_icon} {title}"

def safe_get_nested(data, keys, default=None):
    """
    Safely get nested dictionary values
    Usage: safe_get_nested(data, ['roadmaps', 0, 'title'], 'Default Title')
    """
    try:
        current = data
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key, {})
            elif isinstance(current, list) and isinstance(key, int):
                if 0 <= key < len(current):
                    current = current[key]
                else:
                    return default
            else:
                return default
        return current if current != {} else default
    except (KeyError, TypeError, IndexError):
        return default