import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich import box 
from rich.table import Table
# Import all modules
from data_manager import load_data
from ui_components import (
    show_welcome_animation, create_menu_panel, create_stats_display, 
    show_motivational_tip
)

from roadmap_operations import (
    create_roadmap, add_step, mark_step_complete, edit_roadmap, 
    delete_roadmap_or_step, sort_roadmaps , show_help
)
from category_manager import manage_categories
from progress_tracker import view_roadmaps, view_progress, Categories, Progress_Visualization
from import_export import import_export_roadmaps


def main():
    console = Console()
    data = load_data()
    
    # Show welcome animation on first run
    show_welcome_animation()
    
    while True:
        console.clear()
        
        # Create main header
        header = Panel.fit(\
            "[bold bright_cyan]🎯 Learning Roadmap Builder 🎯[/bold bright_cyan]",
            subtitle="[dim]Your Personal Learning Companion[/dim]",
            border_style="bright_cyan",
            box=box.DOUBLE
        )
        console.print(header, justify="center")
        console.print()
        
        # Show user stats
        if data["roadmaps"]:
            stats_panel = create_stats_display(data)
            console.print(stats_panel)
            console.print()
        
        menu_panels = create_menu_panel()
        if len(menu_panels) == 1:
           # Single column layout
           console.print(menu_panels[0])
        else:
           # Multi-column layout (only if terminal is wide enough)
           try:
             columns = Columns(menu_panels, equal=True, expand=True)
             console.print(columns)
           except:
            # Fallback to single column if columns don't fit
            for panel in menu_panels:
              console.print(panel)
            console.print()
    
        tip_panel = show_motivational_tip()
        console.print(tip_panel)
    
        console.print(Panel.fit(
            "[dim]✨ Created by [/dim][bold blink bold grey11]joy[/] [dim]• [/dim]"
            "[blue]GitHub: @Unknown22X[/blue]",
            border_style="dim",
            box=box.SIMPLE
        ))    
        choice_prompt = Text()
        choice_prompt.append("🎮 Select your choice", style="bold bright_white")
        choice_prompt.append(" (1-13): ", style="dim")
        
        console.print(choice_prompt, end="")
        choice = input().strip()
        
        if choice.isdigit():
            idx = int(choice)
            
            # Add loading animation for better UX
            if idx in range(1, 14):

                console.print(f"\n[dim]Loading option {idx}...[/dim]")
                time.sleep(0.5)
            
            match idx:
                case 1:
                    console.clear()
                    view_roadmaps(data)
                    console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
                    input()
                case 2:
                    console.clear()
                    create_roadmap(data)
                    console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
                    input()
                case 3:
                    console.clear()
                    add_step(data)
                    console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
                    input()
                case 4:
                    console.clear()
                    mark_step_complete(data)
                    console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
                    input()
                case 5:
                    console.clear()
                    delete_roadmap_or_step(data)
                    console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
                    input()
                case 6:
                    console.clear()
                    view_progress(data)
                    console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
                    input()
                case 7:
                    console.clear()
                    sort_roadmaps(data)
                    console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
                    input()
                case 8:
                    console.clear()
                    manage_categories(data)
                case 9:
                    console.clear()
                    Categories(data)
                    console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
                    input()
                case 10:
                    Progress_Visualization(data)
                    console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
                    input()
                case 11:
                    console.clear()
                    edit_roadmap(data)
                    console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
                    input()
                case 12:
                    console.clear()
                    import_export_roadmaps(data)
                    console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
                    input()
                case 13:
                    # Stylish exit sequence
                    console.clear()
                    goodbye_panel = Panel.fit(
                        "[bold bright_green]🎉 Thank you for using Learning Roadmap Builder! 🎉[/bold bright_green]\n"
                        "[dim]Keep learning and growing! 🚀[/dim]",
                        border_style="bright_green",
                        box=box.DOUBLE
                    )
                    console.print(goodbye_panel, justify="center")
                    console.print("\n[dim]Saving your progress...[/dim]")
                    time.sleep(1)
                    console.print("[green]✅ Progress saved successfully![/green]")
                    time.sleep(0.5)
                    show_help()
                    time.sleep(5.0)
                    console.print("[bright_blue]👋 See you next time![/bright_blue]")
                    break
                case _: 
                    console.print(f"\n[bold red]❌ Invalid choice![/bold red] Please select a number between [bold]1[/bold] and [bold]13[/bold].")
                    time.sleep(2)
        else:
            console.print(f"\n[bold red]❌ Invalid input![/bold red] Please enter a [bold]number[/bold].")
            time.sleep(2)

if __name__ == "__main__":
    main()


    
