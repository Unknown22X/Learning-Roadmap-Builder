from data_manager import save_data
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm ,PromptError
from rich import box
from rich.table import Table
from config import MOTIVATIONAL_TIPS, ANIMATION_DELAY , PRIORITY_ORDER
import time

def create_roadmap(data):

    console = Console()
    console.clear()
    console.print(Panel.fit("✨ [bold green]Create New Roadmap[/bold green]", subtitle = "[dim]Start your learning journey[/]" , border_style="green" , box=box.DOUBLE))
    console.print()
    categories_table  = Table(show_header=False , box=box.SIMPLE)
    categories_table.add_column("#" , style="bold cyan" ,  width=4)
    categories_table.add_column('Catgory' , style="white")
    # Show available categories
    console.print("[bold]Available categories:[/bold]")
    for i, category in enumerate(data["categories"], start=1):
        categories_table.add_row(str(i) , f"📂 {category}")
    console.print(categories_table)
    console.print(f"[dim]{len(data['categories']) + 1}. Add new category[/dim]")
    console.print()
    # Get category choice
    try:
        cat_choice = IntPrompt.ask(
            "[yellow][bold]Select category number[/bold][/]",
            choices=[str(i) for i in range(1, len(data["categories"]) + 2)],
            show_choices=False
        )
    except PromptError:
     console.print("[red]Invalid selection! Please choose a valid category number.[/red]")
     return
    
    # Handle category selection
    if cat_choice == len(data["categories"]) + 1:
        # Add new category
        new_category =  Prompt.ask("[bold]Enter new category name[/bold]")
        if new_category:
            data["categories"].append(new_category)
            category = new_category
            console.print(f"[green]✅ Category '{new_category}' added.[/]")
        else:
            category = "Other"
            console.print("[yellow]Using 'Other' category[/yellow]")
    else:
        category = data["categories"][cat_choice - 1]
        console.print(f"[cyan]Selected: 📂 {category}[/cyan]")
    # Get roadmap title
    title = Prompt.ask("[bold]Enter roadmap title[/bold]")
    if not title or title.isspace():
        console.print("[red]❌ Title cannot be empty or just spaces.[/]")
        return
    if title:
        data["roadmaps"].append({
            "title": title, 
            "category": category,
            "steps": []
        })
        save_data(data)
    console.print(Panel.fit(
        f"✅ [bold green]Roadmap '{title}' created![/bold green]",
        subtitle=f"[dim]Category: {category}[/dim]",
        border_style="bright_green",
        box=box.ROUNDED
    ))
def add_step(data):
    console = Console()
    console.print(Panel.fit("[bold green]➕ Add Step[/bold green]", border_style="green", box=box.DOUBLE))
    roadmaps = data["roadmaps"]
    if not roadmaps:
        console.print("[yellow][bold]No roadmaps available.[/bold][/]")
        console.print("[dim][yellow]Try option 2 to create a roadmap[/][/]")
        return
    table = Table(title="🗺️   Select Roadmap", box=box.ROUNDED)
    table.add_column("#", style="bold cyan", width=4, justify="center")
    table.add_column("Title", style="bold orchid")
    for i, roadmap in enumerate(roadmaps, start=1):
        table.add_row(str(i), roadmap["title"])
    console.print(table)
    console.print()

    while True:
        val = Prompt.ask("[bold cyan]Enter roadmap number (or 'q' to quit)[/]", show_choices=False)
        if val == "q":
           return
        try:
         idx = int(val) - 1
         if idx < 0 or idx >= len(roadmaps):
            print("[red]Invalid selection.[/red]")
         else:
            break
        except ValueError:
            print("[red]Please enter a number or 'q' to quit.[/red]")

    console.print()
    step_title = Prompt.ask("[bold]Enter step title[/bold]").strip()
    if not step_title:
        console.print("[red]❌ Step title cannot be empty.[/red]")
        return
    
    try:
        priority_choice = IntPrompt.ask("[bold]Priority : 1 ~ high , 2 ~ medium , 3 ~ low, 4 ~ none[/bold]", choices=["1", "2", "3", "4"])
        priority_map = {1: "high", 2: "medium", 3: "low", 4: "none"}
        priority = priority_map[priority_choice]
    except:
        priority = "none"
    roadmaps[idx]["steps"].append({"title": step_title, "done": False , "priority" : priority })
    with console.status("[bold green]Saving...[/]"):
        save_data(data)
        time.sleep(0.5)
    console.print(Panel.fit(
        f"✅ [bold green]Step '{step_title}' added to '{roadmaps[idx]['title']}'.[/]",
        border_style="bright_green",
        box=box.ROUNDED
    ))
def mark_step_complete(data):

    console = Console()
    console.clear()
    console.print(Panel.fit("✨ [bold green]Mark step complate[/bold green]" , border_style="pale_green1" , box=box.DOUBLE))
    # select which task 
    roadmaps = data["roadmaps"]
    if not roadmaps:
        console.print("[red]❌ No roadmaps avaiable[/]")
        return
    
    table = Table(title="🗺️   Select Roadmap", box=box.ROUNDED)
    table.add_column("#", style="bold plum2", width=4, justify="center")
    table.add_column("Title", style="bold grey82")

    for i, roadmap in enumerate(roadmaps, start=1):
        table.add_row(str(i), roadmap["title"])
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

    # select which step : 
    steps = roadmaps[idx]["steps"]
    if not steps:
        console.print("[bold yellow]This roadmap has no steps yet.[/]")
        return
    
    table = Table(title="🗺️   Select a step", box=box.ROUNDED)
    table.add_column("#", style="bold light_steel_blue", width=4, justify="center")
    table.add_column("Title", style="bold hot_pink3")

    for i, step in enumerate(steps, start=1):
        table.add_row(str(i), step["title"])
    console.print(table)
    console.print()
    while True:
        val = Prompt.ask("[bold cyan]Enter step number (or 'q' to quit)[/]", show_choices=False)
        if val == "q":
           return
        try:
         idxs = int(val) - 1
         if idxs < 0 or idxs >= len(roadmaps):
            console.print("[red]Invalid selection.[/red]")
         else:
            break
        except ValueError:
            console.print("[red]Please enter a number or 'q' to quit.[/red]")
    # save the updated data
    steps[idxs]["done"] = not steps[idxs]["done"]
    state = "complete" if steps[idxs]["done"] else "incomplete"
    with console.status("[bold green]Saving...[/]"):
        save_data(data)
        time.sleep(0.5)
    console.print(Panel.fit(
        f"✅ [bold green]Step '{steps[idxs]['title']}' marked as {state}.[/]",
        border_style="bright_green",
        box=box.ROUNDED
    ))
    

def get_highest_priority_score(roadmap):
    """Get numerical score for roadmap's highest priority step"""
    if not roadmap.get("steps"):
        return 3 
    
    return min(
        PRIORITY_ORDER.get(step.get("priority", "none"), 3)
        for step in roadmap["steps"]
    )
def sort_by_priority(items, is_roadmap=False):
    """
    Sort by priority - works for both steps and roadmaps
    items: either list of steps or list of roadmaps
    is_roadmap: True if sorting roadmaps, False if sorting steps
    """
    if is_roadmap:
        # Sort roadmaps by their highest priority step
        return sorted(items, key=lambda roadmap: get_highest_priority_score(roadmap))
    else:
        # Sort steps within a roadmap
        return sorted(items, key=lambda step: PRIORITY_ORDER.get(step.get("priority", "none"), 3))

def sort_roadmaps(data):
    console = Console()
    console.print(Panel.fit("[red]🗃️  Sort Roadmaps[/]", border_style="red", box=box.DOUBLE))
    
    if not data["roadmaps"]:
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

    if choice == "1":
        data["roadmaps"].sort(key=lambda x: x["title"].lower())
    elif choice == "2":
        data["roadmaps"].sort(key=lambda x: sum(1 for s in x["steps"] if s["done"]) / len(x["steps"]) if x["steps"] else 0, reverse=True)
    elif choice == "3":
        data["roadmaps"].sort(key=lambda x: x.get("category", "Uncategorized"))
    elif choice == "4": 
        # Sort roadmaps by priority
        data["roadmaps"] = sort_by_priority(data["roadmaps"], is_roadmap=True)
        
        # Sort steps within each roadmap by priority
        for roadmap in data["roadmaps"]:
            if roadmap["steps"]:
                roadmap["steps"] = sort_by_priority(roadmap["steps"], is_roadmap=False)
    
    with console.status("[bold green]Saving...[/]"):
        save_data(data)
        time.sleep(0.5)
    
    console.print(Panel.fit(
        f"✅ [bold green]Roadmaps have been sorted.[/]",
        border_style="bright_green", 
        box=box.ROUNDED
    ))
def edit_roadmap(data):
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
    
    roadmaps = data["roadmaps"]
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
        steps_count = len(roadmap.get("steps", []))
        category = roadmap.get("category", "Uncategorized")
        roadmap_table.add_row(str(i), roadmap["title"], category, str(steps_count))
    
    console.print(roadmap_table)
    console.print()

    # Get roadmap selection
    try:
        roadmap_num = IntPrompt.ask(
            "[bold]Select roadmap number[/bold]",
            choices=[str(i) for i in range(1, len(roadmaps) + 1)] + ["q"],
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
            
        old_title = roadmaps[roadmap_idx]["title"]
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
        steps = roadmaps[roadmap_idx]["steps"]
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
            status = "✅ Done" if step.get("done", False) else "⏳ Pending"
            steps_table.add_row(str(i), step["title"], status)
        
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
            
        old_step_title = steps[step_idx]["title"]
        steps[step_idx]["title"] = new_step_title.strip()
        
        with console.status("[bold green]Saving changes...[/]"):
            save_data(data)
            time.sleep(0.5)
        
        console.print()
        console.print(Panel.fit(
            f"✅ [bold green]Step updated![/bold green]",
            subtitle=f"[dim]From '{old_step_title}' to '{new_step_title} '[/dim]",
            border_style="bright_green",
            box=box.ROUNDED
        ))

def delete_roadmap_or_step(data):
    console= Console()
    console.print(Panel.fit("[red]🗑️  Delete Roadmap/Step[/]" , border_style="red" , box=box.DOUBLE))
    try:
        oper = IntPrompt.ask(
            "[yellow][bold]Enter 1 to delete a roadmap , 2 to delete a step[/][/]",
            choices=[str(i) for i in range(1, 3)],
            show_choices=False
        )
    except:
        console.print("[red]Invalid selection![/red]")
        return
         
    roadmaps = data["roadmaps"]
    if not roadmaps:
        console.print("[yellow][bold]No roadmaps available.[/bold][/]")
        console.print("[dim][yellow] press 3 to add a step [/][/] ")
        return
    
    roadmap_table = Table(title="🗺️  Select roadmap" , box = box.ROUNDED)
    roadmap_table.add_column("#" , style=" bold cyan" , width=4 , justify="center")
    roadmap_table.add_column("Roadmap" , style="bold orchid", justify='center')
    for i, roadmap in enumerate(roadmaps, start=1):
        roadmap_table.add_row(str(i) , str(roadmap["title"]))
    console.print(roadmap_table)
    console.print()

    try:
        roadmap_idx = IntPrompt.ask(
            "[red][bold]Select Roadmap number[/bold][/]",
            choices=[str(i) for i in range(1, len(data["roadmaps"]) + 1)],
            show_choices=True
        )
        roadmap_idx = roadmap_idx - 1 
    except:
        console.print("[red]Invalid selection![/red]")
        return
    

    if oper == 1:  
        try : 
            confirm = Prompt.ask(f"[bold][yellow]⚠️   Are you sure you want to delete '{roadmaps[roadmap_idx]['title']}'? (y/n): [/][/]" , choices=["y" ,"N"] ,show_choices=False , case_sensitive=False)

        except:
            console.print("[red]Invalid selection![/red]")
            return
        if confirm != "y":
            console.print("[green]Deletion canceled. [green]")
            return
        deleted = roadmaps.pop(roadmap_idx)
        save_data(data)
        console.print(Panel.fit(f"✅ [bold green] Roadmap '{deleted['title']}' deleted.[/]" , border_style="bright_green" ,box=box.ROUNDED))

    elif oper == 2:
        steps = roadmaps[roadmap_idx]["steps"]
        if not steps:
            console.print("[bold yellow]This roadmap has no steps yet. [/]" , justify='center')
            return
       
        steps_table = Table(title="🗺️ Select a step" , box = box.ROUNDED )
        steps_table.add_column("#" , style=" bold cyan" , width=4 , justify="center")  
        steps_table.add_column("Title" , style="bold violet")
        console.print()
        for i,step in enumerate(steps, start=1) : 
            steps_table.add_row(str(i) , step["title"])
        console.print(steps_table)
        step_num= 0
        try :
            step_num = IntPrompt.ask(f"[bold cyan]Enter a step[/]" ,choices=[str(i) for i in range(1,len(steps)+1)] , show_choices= False)
            console.print()
        except:
            console.print("[red]❌ Invalid input. Please enter a valid number.[/]")
            return
        idxS= int(step_num) 
        idxS -=1
        confirm = Confirm.ask(f"Are you sure you want to delete '{steps[idxS]['title']}'? " , console=console)
        if confirm :
            deleted = steps.pop(idxS)
            with console.status("[bold green]Saving...[/]"):
             
             save_data(data)
             time.sleep(0.5)  
            console.print(f"[bold green]Step '{deleted['title']}' deleted from roadmap '{roadmaps[roadmap_idx]['title']}'.[/]")
        else : 
            console.print(f"[bold red]Deletion canceled.[/]")
            return
def search (data) :
    """Search Roadmaps by title , catgoary or step content"""
    console = Console()
    console.clear()
    console.print(Panel.fit(
        "[bold cyan] Search Roadmpas & Steps [/]" ,
        subtitle="Find your learning content" , 
        border_style= "cyan", 
        box=box.DOUBLE
                            ))
    console.print()
    if not data["roadmaps"] :
        console.print("[bold red] No roadmaps available.[/]")
        console.print("[dim][yellow]Try option 2 to create a roadmap[/][/]")
        return
    try :
        keyword = Prompt.ask("🔍 Enter search keyword ").strip().lower()
        if not keyword :
            console.print("[red] Search keyword cannot be empty[/]")
            return
    except PromptError: 
        console.print("[red]Invalid input! Please enter a valid keyword.[/red]")
        return
    
    # Collect matches

    roadmaps_results= []
    steps_results = []
    for roadmap in data["roadmaps"] :
        match_reasons= []
        # if it a roadmap
        if keyword in roadmap["title"].lower() :
            match_reasons.append("Title")
        if keyword in roadmap.get("category" ,"").lower() :
            match_reasons.append("Category")
        # serarch in steps : 
        match_steps=[step for step in roadmap["steps"] if keyword in step["title"].lower()]
        if match_steps : 
            match_reasons.append("step")
            steps_results.extend([(roadmap,step) for step in match_steps])
        if match_reasons:
            roadmaps_results.append((roadmap, ", ".join(match_reasons)))
     # display results 
    if not roadmaps_results and not steps_results :
          console.print(f"[red]No matches found for '{keyword}'.[/red]")
          return        
    if roadmaps_results: 
            console.print(f"\n [cyan bold]Found {len(roadmaps_results)} roadmap(s) matching '{keyword}'[/]")
            table = Table(title="🗺️   Roadmap Search Results" , box =box.ROUNDED , style = "red")  
            table.add_column("#", style="bold cyan", width=4, justify="center") 
            table.add_column("Title", style="bold orchid")
            table.add_column("Category", style="white")
            table.add_column("Progress", style="green", justify="center")
            table.add_column("Matched On", style="yellow")
            for i, (roadmap,reasons)in enumerate(roadmaps_results, start = 1) :

                completed = sum(1 for step in roadmap.get("steps" , []) if step.get("done" , False) )
                percent  = (completed / len(roadmap["steps"])) * 100 if len(roadmap["steps"]) > 0 else 0
                table.add_row(str(i),roadmap["title"] , roadmap.get("category" ,"other") ,f"{percent:.1f}%" , reasons)
            console.print(table)
    if steps_results : 
                console.print(f"\n[bold cyan]Found {len(steps_results)} step(s) matching '{keyword}'[/bold cyan]")
                table = Table(title="📝 Step Search Results", box=box.ROUNDED)
                table.add_column("#",style="bold cyan", width=4, justify="center")
                table.add_column("Step Title", style="bold violet")
                table.add_column("Roadmap", style="white")
                table.add_column("Status", style="green")
                for i , (roadmap,step) in enumerate (steps_results, start = 1) :
                    status = "✅ Done" if step.get("done", False) else "❌ Not Done"
                    table.add_row(str(i),step["title"],roadmap["title"] , status)
                console.print(table)
def show_help():
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
        "• [green]Telegram: WE_CX [/green]\n"
        # "• [cyan]Portfolio: myportfolio.com[/cyan]"
        ,
        border_style="bright_blue",
        box=box.ROUNDED
    ))