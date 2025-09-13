from data_manager import save_data
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import box
from rich.table import Table
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
    roadmaps[idx]["steps"].append({"title": step_title, "done": False})
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
    



def sort_roadmaps(data):
    console= Console()
    console.print(Panel.fit("[red]🗃️  Sort Roadmaps[/]" , border_style="red" , box=box.DOUBLE))
    if not data["roadmaps"]:
        console.print("[red]No roadmaps to sort.[/]")
        return
 
    table = Table( )
    table.add_column("#")
    table.add_column("Option")
    table.add_row("1" ,"Sort by title" )
    table.add_row("2" ,"Sort by progress" )
    table.add_row("3" ,"Sort by category" )
    console.print(table)
    try:
        choice = IntPrompt.ask(
            "[yellow][bold]Select option",
            choices=[str(i) for i in range(1, 4)],
            show_choices=True
        )
    except:
        console.print("[red]❌  Invalid selection![/red]")
        return

    if choice == "1":
        data["roadmaps"].sort(key=lambda x: x["title"].lower())
    elif choice == "2":
        data["roadmaps"].sort(key=lambda x: sum(1 for s in x["steps"] if s["done"]) / len(x["steps"]) if x["steps"] else 0, reverse=True)
    elif choice == "3":
        data["roadmaps"].sort(key=lambda x: x.get("category", "Uncategorized"))
    with console.status("[bold green]Saving...[/]") :
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
