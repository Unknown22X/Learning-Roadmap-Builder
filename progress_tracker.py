from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text
from rich.columns import Columns
from ui_components import get_motivational_message
from config import PRIORITY_EMOJIS , PRIORITY_COLORS

def view_roadmaps(data):
    console = Console()
    console.clear()
    
    # beautiful header
    console.print(Panel.fit(
        "📋 [bold bright_cyan]View All Roadmaps[/bold bright_cyan]", 
        subtitle="[dim]Your Learning Journeys[/dim]",
        border_style="bright_cyan",
        box=box.DOUBLE
    ))
    console.print()
    
    if not data["roadmaps"]:
        console.print(Panel.fit(
            "[italic yellow]No roadmaps found.[/italic yellow]\n"
            "[dim]Create your first roadmap to start your learning journey![/dim]",
            border_style="yellow",
            box=box.ROUNDED
        ))
        return
    
    # Option to filter by category
    console.print("[bold]View options:[/bold]")
    console.print("1. [cyan]View all roadmaps[/cyan]")
    console.print("2. [cyan]View by category[/cyan]")
    console.print()
    
    choice = input("Select option (1 or 2): ").strip()
    
    if choice == "2":
        view_roadmaps_by_category(data)
    else:
        view_all_roadmaps(data)

def view_all_roadmaps(data):
    console = Console()
    
    if not data["roadmaps"]:
        console.print(Panel.fit(
            "[italic yellow]No roadmaps found.[/italic yellow]",
            border_style="yellow",
            box=box.ROUNDED
        ))
        return

    for roadmap in data["roadmaps"]:
        # Calculate progress percentage
        steps = roadmap.get("steps", [])
        total = len(steps)
        completed = sum(1 for step in steps if step.get("done", False))
        percent = (completed / total * 100) if total > 0 else 0
        
        # Determine status color based on progress
        if percent == 0:
            status_color = "red"
            status_emoji = "💤"
        elif percent < 50:
            status_color = "yellow"
            status_emoji = "🌱"
        elif percent < 100:
            status_color = "green"
            status_emoji = "🚀"
        else:
            status_color = "bright_green"
            status_emoji = "🎉"
        
        # Create roadmap header
        console.print(Panel.fit(
            f"{status_emoji} [bold]{roadmap.get('title', 'Untitled')}[/bold] [dim]({roadmap.get('category', 'Uncategorized')})[/dim]",
            subtitle=f"[{status_color}]{percent:.1f}% complete[/{status_color}]",
            border_style=status_color,
            box=box.ROUNDED
        ))
        
        if steps:
            # Create steps table
            steps_table = Table(show_header=True, box=box.SIMPLE, show_lines=True)
            steps_table.add_column("#", style="bold", width=4, justify="center")
            steps_table.add_column("Priority", style="bold", width=8, justify="center")            
            steps_table.add_column("Step", style="bold white")
            steps_table.add_column("Status", style="bold", width=12, justify="center")

            for i, step in enumerate(steps, start=1):

                priority = step.get("priority", "none")
                priority_emoji = PRIORITY_EMOJIS.get(priority, "📝")
                priority_color = PRIORITY_COLORS.get(priority, "dim")
                
                if step.get("done", False):
                    status = "[green]✅ Done[/green]"
                else:
                    status = "[yellow]⏳ Pending[/yellow]"
                steps_table.add_row(str(i), f"[{priority_color}]{priority_emoji}[/{priority_color}]", step['title'], status)
            
            console.print(steps_table)

        else:
            console.print(Panel.fit(
                "[italic dim]No steps added yet. Use option 3 to add steps.[/italic dim]",
                border_style="dim",
                box=box.SIMPLE
            ))
        
        # Progress summary
        progress_bar = create_progress_bar(percent, 40)
        console.print(f"\n📊 Progress: [bold]{completed}/{total}[/bold] steps")
        console.print(progress_bar)
        console.print(f"🎯 Status: [{status_color}]{get_progress_status(percent)}[/{status_color}]")
        console.print("\n" + "="*60 + "\n")

def create_progress_bar(percent, width=40):
    """Create a visual progress bar"""
    filled = int(width * percent / 100)
    empty = width - filled
    
    progress_bar = "[green]" + "█" * filled + "[/green]"
    progress_bar += "[dim]" + "░" * empty + "[/dim]"
    progress_bar += f" [bold]{percent:.1f}%[/bold]"
    
    return progress_bar

def get_progress_status(percent):
    """Get descriptive status based on percentage"""
    if percent == 0:
        return "Not started"
    elif percent < 25:
        return "Just beginning"
    elif percent < 50:
        return "Making progress"
    elif percent < 75:
        return "Good pace!"
    elif percent < 100:
        return "Almost there!"
    else:
        return "Completed! 🎉"
    
def view_roadmaps_by_category(data):
    console = Console()
    
    if not data["categories"]:
        console.print(Panel.fit(
            "[italic yellow]No categories available.[/italic yellow]",
            border_style="yellow",
            box=box.ROUNDED
        ))
        return
    
    # Create category selection table
    cat_table = Table(title="📂 Select Category", show_header=True, box=box.ROUNDED)
    cat_table.add_column("#", style="bold cyan", width=4, justify="center")
    cat_table.add_column("Category", style="bold white")
    cat_table.add_column("Roadmaps", style="green", justify="center")
    
    for i, category in enumerate(data["categories"], start=1):
        count = sum(1 for roadmap in data["roadmaps"] if roadmap.get("category") == category)
        cat_table.add_row(str(i), category, str(count))
    
    console.print(cat_table)
    console.print()
    
    while True:
        choice = input("Enter category number: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(data["categories"]):
                category = data["categories"][choice - 1]
                break
        console.print("[red]Invalid input. Please enter a valid number.[/red]")
    
    # Filter roadmaps by category
    category_roadmaps = [r for r in data["roadmaps"] if r.get("category") == category]
    
    if not category_roadmaps:
        console.print(Panel.fit(
            f"[italic yellow]No roadmaps found in category '{category}'.[/italic yellow]",
            border_style="yellow",
            box=box.ROUNDED
        ))
        return
    
    console.print(Panel.fit(
        f"📂 [bold bright_cyan]{category}[/bold bright_cyan] Roadmaps",
        border_style="bright_cyan",
        box=box.DOUBLE
    ))
    console.print()
    
    for roadmap in category_roadmaps:
        steps = roadmap.get("steps", [])
        total = len(steps)
        completed = sum(1 for step in steps if step.get("done", False))
        percent = (completed / total * 100) if total > 0 else 0
        
        # Determine status color
        if percent == 0:
            status_color = "red"
        elif percent < 50:
            status_color = "yellow"
        elif percent < 100:
            status_color = "green"
        else:
            status_color = "bright_green"
        
        console.print(Panel(
            f"📝 [bold]{roadmap['title']}[/bold]\n"
            f"📊 Progress: [bold]{completed}/{total}[/bold] steps\n"
            f"🎯 Status: [{status_color}]{percent:.1f}% complete[/{status_color}]",
            box=box.SIMPLE,
            border_style=status_color
        ))
        console.print()
def get_priority_display(step):
    """Get formatted priority display for a step"""
    priority = step.get("priority", "none")
    return f"[{PRIORITY_COLORS[priority]}]{PRIORITY_EMOJIS[priority]}[/{PRIORITY_COLORS[priority]}]"
def view_progress(data):
    console =Console()
    console.print(Panel.fit("[bold light_steel_blue3]View progress[/]" , box= box.ROUNDED))
    if not data["roadmaps"]:
        console.print("[bold red]No roadmaps found.[/]")
        return
    roadmaps_table = Table(title="[bold blue]Progress Summary[/bold blue]", show_header=True, header_style="bold magenta")
    roadmaps_table.add_column("Roadmap", style="cyan")
    roadmaps_table.add_column("Progress", justify="center", style="light_sky_blue1") 
    roadmaps_table.add_column("Steps", justify="center", style="deep_pink4")
    roadmaps_table.add_column("Priority", justify="center", style="yellow")  # New column

    for roadmap in data["roadmaps"]:
        if "title" not in roadmap or "steps" not in roadmap :
            continue
        steps = roadmap["steps"]
        total = len(steps)
        completed = sum(1 for step in steps if step["done"])
        percent = (completed / total * 100) if total > 0 else 0
        high_priority_steps = sum(1 for step in steps if step.get("priority") == "high")
        roadmaps_table.add_row(roadmap["title"], f"{percent:.1f}%", f"{completed}/{total}", f"🚨{high_priority_steps}")

        
    console.print(roadmaps_table)

def Categories(data):
    console = Console()
    console.print("\n[bold][Category Progress][/]")
    if not data["categories"]:
        console.print("[red]No categories found.[/]")
        return
    
    table = Table(title="Category Progress", show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan", justify="center")
    table.add_column("Roadmaps")
    table.add_column("Steps Completed", justify="center")
    table.add_column("Progress", justify="center")
    
    for category in data["categories"]:
        roadmaps = [r for r in data["roadmaps"] if r.get("category") == category]
        total_roadmaps = len(roadmaps)
        total_steps = sum(len(r["steps"]) for r in roadmaps)
        completed_steps = sum(sum(1 for s in r["steps"] if s["done"]) for r in roadmaps)
        percent = (completed_steps / total_steps * 100) if total_steps > 0 else 0
        table.add_row(category, str(total_roadmaps), f"{completed_steps}/{total_steps}", f"{percent:.1f}%")
    
    console.print(table)

def Progress_Visualization(data):
    console = Console()
    
    # Clear screen and create a beautiful header
    console.clear()
    console.print(Panel.fit("🎯 [bold cyan]Learning Progress Dashboard[/bold cyan] 🎯", 
                          style="bold blue", subtitle="Track your learning journey"))
    
    if not data["roadmaps"]:
        console.print("\n[italic yellow]No roadmaps found. Create your first roadmap to start tracking progress![/italic yellow]")
        console.print("\n💡 [dim]Tip: Use option 2 to create a new roadmap[/dim]")
        return
    
    # Create overall statistics
    total_roadmaps = len(data["roadmaps"])
    total_steps = sum(len(roadmap.get("steps","")) for roadmap in data["roadmaps"])
    completed_steps = sum(sum(1 for step in roadmap.get("steps","") if step["done"]) for roadmap in data["roadmaps"])
    overall_percent = (completed_steps / total_steps * 100) if total_steps > 0 else 0
    
    # Overall progress panel
    overall_panel = Panel(
        f"""📊 [bold]Overall Progress:[/bold] [green]{overall_percent:.1f}%[/green]
        
├─ 🗺️  Roadmaps: [cyan]{total_roadmaps}[/cyan]
├─ 📝 Total Steps: [white]{total_steps}[/white]
├─ ✅ Completed: [green]{completed_steps}[/green]
└─ ⏳ Remaining: [yellow]{total_steps - completed_steps}[/yellow]""",
        title="📈 Overall Statistics",
        border_style="cyan",
        box=box.ROUNDED
    )
    
    console.print(overall_panel)
    console.print()  # Spacer
    
    # Display each roadmap  
    for roadmap in data["roadmaps"]:
        if "steps" not in roadmap: 
             console.print(f"[red bold] Warning: found a roadmap missing title or steps, skipping it. [/]")
             continue
        steps = roadmap["steps"]
        total = len(steps)
        completed = sum(1 for step in steps if step["done"])
        percent = (completed / total * 100) if total > 0 else 0
        
        # Determine status and colors
        if percent == 0:
            status_emoji, status_color, status_msg = "💤", "red", "Not started"
        elif percent < 25:
            status_emoji, status_color, status_msg = "🌱", "yellow", "Beginning"
        elif percent < 50:
            status_emoji, status_color, status_msg = "🚶‍♂️", "blue", "Progressing"
        elif percent < 75:
            status_emoji, status_color, status_msg = "🚀", "green", "Good pace!"
        elif percent < 100:
            status_emoji, status_color, status_msg = "🔥", "bright_green", "Almost there!"
        else:
            status_emoji, status_color, status_msg = "🎉", "bold green", "Completed!"
        
        # Create  progress bar with gradient
        bar_width = 30
        filled_segments = int(bar_width * percent / 100)
        progress_bar = ""
        
        # Create gradient effect
        for i in range(bar_width):
            if i < filled_segments:
                # Gradient from green to bright green
                if i < filled_segments * 0.3:
                    color = "green"
                elif i < filled_segments * 0.6:
                    color = "bright_green"
                else:
                    color = "bold green"
                progress_bar += f"[{color}]█[/{color}]"
            else:
                progress_bar += "[dim]░[/dim]"
        
        # Create the main content table
        content_table = Table.grid()
        content_table.add_column(width=35)
        content_table.add_column(width=50)
        
        # Progress bar and stats
        progress_section = Table(show_header=False, box=None, show_lines=True)
        progress_section.add_row(f"{status_emoji} [bold]{roadmap['title']}[/bold]")
        progress_section.add_row(f"{progress_bar} [bold {status_color}]{percent:.1f}%[/bold {status_color}]")
        progress_section.add_row(f"📊 [dim]{completed}/{total}[/dim] steps • 🎯 [dim]{status_msg}[/dim]")
        
        # Completed steps list (if any)
        if completed > 0:
            completed_steps_list = Table(show_header=False, box=None)
            completed_steps_list.add_row("[green]✅ Completed:[/green]")
            for step in steps:
                if step["done"]:
                    priority = step.get("priority", "none")
                    emoji = PRIORITY_EMOJIS.get(priority, "📝")
                    color = PRIORITY_COLORS.get(priority, "dim")
                    completed_steps_list.add_row(f"   🟢 [{color}]{emoji}[/{color}] {step['title']}")
        
        # Pending steps list (if any)
        if completed < total:
            pending_steps_list = Table(show_header=False, box=None)
            pending_steps_list.add_row("[yellow]⏳ Pending:[/yellow]")
            for step in steps:
                if not step["done"]:
                    priority = step.get("priority", "none") 
                    emoji = PRIORITY_EMOJIS.get(priority, "📝")
                    color = PRIORITY_COLORS.get(priority, "dim")
                pending_steps_list.add_row(f"   🔴 [{color}]{emoji}[/{color}] {step['title']}")
        
        # Combine everything
        content_table.add_row(progress_section)
        
        if completed > 0:
            content_table.add_row(completed_steps_list)
        if completed < total:
            content_table.add_row(pending_steps_list)
        
        # Create the panel
        roadmap_panel = Panel(
            content_table,
            title=f"[bold]📋 {roadmap['title']}[/bold]",
            subtitle=f"[dim]{len(steps)} steps[/dim]",
            border_style=status_color,
            box=box.ROUNDED,
            padding=(1, 2)
        )
        
        console.print(roadmap_panel)
        console.print()  # Spacer
    
    # Add motivational message based on overall progress
    from ui_components import get_motivational_message
    motivational_msg = get_motivational_message(overall_percent)
    console.print(Panel.fit(f"💪 [italic]{motivational_msg}[/italic]", 
                          border_style="yellow", box=box.ROUNDED))
    
    # Add quick tips
    console.print("\n[dim]💡 Tips: Use '[white]4[/white]' to mark steps complete • '[white]7[/white]' to sort roadmaps • '[white]8[/white]' to manage categories[/dim]")