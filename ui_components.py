import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn
from rich import box
from config import MOTIVATIONAL_TIPS, ANIMATION_DELAY
from data_manager import get_user_stats

def show_welcome_animation():
    """Display an animated welcome screen"""
    console = Console()
    console.clear()
    
    # Animated title
    title_frames = [
        "🎯 Learning Roadmap Builder",
        "🎯 Learning Roadmap Builder ✨",
        "🎯 Learning Roadmap Builder ✨🚀",
        "🎯 Learning Roadmap Builder ✨🚀💡"
    ]
    
    for frame in title_frames:
        console.clear()
        console.print(Panel.fit(
            f"[bold bright_blue]{frame}[/bold bright_blue]",
            border_style="bright_blue",
            box=box.DOUBLE
        ), justify="center")
        time.sleep(ANIMATION_DELAY)
    
    # Welcome message
    welcome_text = Text()
    welcome_text.append("Welcome to your personal learning companion! ", style="bright_cyan")
    welcome_text.append("🌟", style="yellow")
    
    console.print()
    console.print(Align.center(welcome_text))
    console.print()
    time.sleep(1)
def create_menu_panel():
    """Create a beautiful 4-column menu with proper spacing"""
    # Create menu sections with optimized widths
    view_section = Table(show_header=False, box=None, padding=(0, 1), width=32)
    view_section.add_row("📋 [bold cyan]1[/bold cyan] View Roadmaps", "Browse paths")
    view_section.add_row("📊 [bold cyan]6[/bold cyan] View Progress", "Check status") 
    view_section.add_row("🎨 [bold cyan]10[/bold cyan] Progress Vis", "Beautiful display")
    
    manage_section = Table(show_header=False, box=None, padding=(0, 1), width=32)
    manage_section.add_row("✨ [bold green]2[/bold green] Create Roadmap", "New journey")
    manage_section.add_row("➕ [bold green]3[/bold green] Add Step", "Add tasks")
    manage_section.add_row("✅ [bold green]4[/bold green] Mark Complete", "Track achievements")
    manage_section.add_row("✏️  [bold green]11[/bold green] Edit", "Modify content")
    
    organize_section = Table(show_header=False, box=None, padding=(0, 1), width=32)
    organize_section.add_row("🗂️  [bold yellow]8[/bold yellow] Manage Categories", "Organize topics")
    organize_section.add_row("📈 [bold yellow]9[/bold yellow] Overview", "View stats")
    organize_section.add_row("🔄 [bold yellow]7[/bold yellow] Sort", "Organize roadmaps")
    
    tools_section = Table(show_header=False, box=None, padding=(0, 1), width=32)
    tools_section.add_row("🔍 [bold magenta]13[/bold magenta] Search Roadmaps/Steps", "Find specific content")
    tools_section.add_row("💾 [bold magenta]12[/bold magenta] Import/Export", "Backup & share")
    tools_section.add_row("🗑️  [bold red]5[/bold red] Delete", "Remove items")
    tools_section.add_row("🚪 [bold white]14[/bold white] Exit", "Save and quit")
    
    # Create panels for each section
    view_panel = Panel(
        view_section, 
        title="[bold bright_blue]📊 View & Track[/bold bright_blue]", 
        border_style="bright_blue", 
        box=box.ROUNDED,
        padding=(0, 0)
    )
    
    manage_panel = Panel(
        manage_section, 
        title="[bold bright_green]🛠️  Create & Manage[/bold bright_green]", 
        border_style="bright_green", 
        box=box.ROUNDED,
        padding=(0, 0)
    )
    
    organize_panel = Panel(
        organize_section, 
        title="[bold bright_yellow]🗂️  Organize[/bold bright_yellow]", 
        border_style="bright_yellow", 
        box=box.ROUNDED,
        padding=(0, 0)
    )
    
    tools_panel = Panel(
        tools_section, 
        title="[bold bright_magenta]🔧 Tools[/bold bright_magenta]", 
        border_style="bright_magenta", 
        box=box.ROUNDED,
        padding=(0, 0)
    )
    
    return [view_panel, manage_panel, organize_panel, tools_panel]

def create_stats_display(data):
    """Create a beautiful stats display"""
    stats = get_user_stats(data)
    
    # Create stats table
    stats_table = Table(show_header=False, box=None)
    stats_table.add_column(justify="center", style="bold")
    stats_table.add_column(justify="center")
    
    # Determine progress emoji and color
    rate = stats["completion_rate"]
    if rate == 0:
        progress_emoji, progress_color = "💤", "red"
        progress_msg = "Ready to start!"
    elif rate < 25:
        progress_emoji, progress_color = "🌱", "yellow" 
        progress_msg = "Getting started"
    elif rate < 50:
        progress_emoji, progress_color = "🚶‍♂️", "blue"
        progress_msg = "Making progress"
    elif rate < 75:
        progress_emoji, progress_color = "🚀", "green"
        progress_msg = "Great momentum!"
    elif rate < 100:
        progress_emoji, progress_color = "🔥", "bright_green"
        progress_msg = "Almost there!"
    else:
        progress_emoji, progress_color = "🎉", "bold green"
        progress_msg = "All completed!"
    
    stats_table.add_row(f"{progress_emoji}", f"[{progress_color}]{rate:.1f}% Complete[/{progress_color}]")
    stats_table.add_row("🗺️", f"[cyan]{stats['roadmaps']}[/cyan] Roadmaps")
    stats_table.add_row("📝", f"[white]{stats['steps']}[/white] Total Steps")
    stats_table.add_row("✅", f"[green]{stats['completed']}[/green] Completed")
    
    return Panel(
        Align.center(stats_table),
        title=f"[bold]{progress_emoji} Your Progress[/bold]",
        subtitle=f"[dim]{progress_msg}[/dim]",
        border_style=progress_color,
        box=box.ROUNDED
    )

def show_motivational_tip():
    """Display a random motivational tip"""
    tip = random.choice(MOTIVATIONAL_TIPS)
    
    return Panel.fit(
        f"[italic bright_yellow]{tip}[/italic bright_yellow]",
        border_style="yellow",
        box=box.ROUNDED
    )

def show_loading_animation():
    """Display a loading animation"""
    console = Console()
    with Progress(
        TextColumn("[bold blue]Loading your progress[/bold blue]"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        transient=True,
    ) as progress:
        task = progress.add_task("", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.02)

def get_motivational_message(percent):
    """Get motivational message based on progress percentage"""
    if percent == 0:
        return "Every expert was once a beginner. Start your journey today! 🚀"
    elif percent < 25:
        return "Great start! Consistency is key. Keep going! 🌟"
    elif percent < 50:
        return "You're making solid progress! The middle is where champions are made. 💪"
    elif percent < 75:
        return "Wow! You're cruising now. Don't stop when you're tired, stop when you're done! 🔥"
    elif percent < 100:
        return "Almost there! The finish line is in sight. One final push! 🏁"
    else:
        return "Incredible! You've completed everything. Time to celebrate and set new goals! 🎊"