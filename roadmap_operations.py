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
    table = Table(title="🗺️ Select Roadmap", box=box.ROUNDED)
    table.add_column("#", style="bold cyan", width=4, justify="center")
    table.add_column("Title", style="bold orchid")
    for i, roadmap in enumerate(roadmaps, start=1):
        table.add_row(str(i), roadmap["title"])
    console.print(table)
    console.print()
    try:
        idx = IntPrompt.ask("[bold cyan]Enter roadmap number (or 'q' to quit)[/]", show_choices=False) - 1
        if idx < 0 or idx >= len(roadmaps):
            raise PromptError
    except PromptError:
        console.print("[red]Invalid selection or quit.[/red]")
        return
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
    print("\n[4] Mark Step Complete")
    # select which task 
    roadmaps = data["roadmaps"]
    if not roadmaps:
        print("No roadmaps available.")
        return
    print("\n=== Select a roadmap by typing its number : \n")
    for i, roadmap in enumerate(roadmaps, start=1):
        print(f"{i}. {roadmap['title']}")
    while True:
        task = input("Enter roadmap number: ").strip()
        if task.isdigit() and 1 <= int(task) <= len(roadmaps):
            idx = int(task) - 1
            break
        print("Invalid input. Please enter a valid number.")

    # select which step : 
    steps = roadmaps[idx]["steps"]
    if not steps:
        print("This roadmap has no steps yet.")
        return

    print("\n=== Select a step by typing its number : \n")
    for i, step in enumerate(steps, start=1):
        print(f"{i}. {step['title']}")
    while True:
        step_num = input("Enter step number : ")
        if step_num.isdigit(): 
            idxS = int(step_num)
            if 1 <= idxS <= len(steps):
                idxS = idxS - 1  # Convert to 0-based for internal use
                break
        print("Invalid input. Please enter a valid number.")
    # save the updated data
    steps[idxS]["done"] = not steps[idxS]["done"]
    state = "complete" if steps[idxS]["done"] else "incomplete"
    save_data(data)
    print(f"Step '{steps[idxS]['title']}' marked as {state}")

def sort_roadmaps(data):
    print("\n[Sort Roadmaps]")
    if not data["roadmaps"]:
        print("No roadmaps to sort.")
        return
    print("1. Sort by title\n2. Sort by progress\n3. Sort by category")
    choice = input("Select option: ").strip()
    if choice == "1":
        data["roadmaps"].sort(key=lambda x: x["title"].lower())
    elif choice == "2":
        data["roadmaps"].sort(key=lambda x: sum(1 for s in x["steps"] if s["done"]) / len(x["steps"]) if x["steps"] else 0, reverse=True)
    elif choice == "3":
        data["roadmaps"].sort(key=lambda x: x.get("category", "Uncategorized"))
    save_data(data)
    print("Roadmaps sorted.")

def edit_roadmap(data):
    print("\n[Edit Roadmap/Step]")
    roadmaps = data["roadmaps"]
    if not roadmaps:
        print("No roadmaps available.")
        return

    print("\nSelect a roadmap to edit:")
    for i, roadmap in enumerate(roadmaps, start=1):
        print(f"{i}. {roadmap['title']}")
    while True:
        roadmap_num = input("Enter roadmap number (or 'q' to quit): ").strip()
        if roadmap_num.lower() == "q":
            return
        if roadmap_num.isdigit() and 1 <= int(roadmap_num) <= len(roadmaps):
            roadmap_idx = int(roadmap_num) - 1
            break
        print("Invalid input. Please try again.")

    print("\nEdit options:")
    print("1. Edit roadmap title")
    print("2. Edit step title")
    while True:
        option = input("Select option: ").strip()
        if option in ("1", "2"):
            break
        print("Invalid input. Please enter 1 or 2.")

    if option == "1":
        new_title = input("Enter new roadmap title: ").strip()
        if new_title:
            old_title = roadmaps[roadmap_idx]["title"]
            roadmaps[roadmap_idx]["title"] = new_title
            save_data(data)
            print(f"Roadmap title changed from '{old_title}' to '{new_title}'.")
        else:
            print("Title cannot be empty.")
    else:
        steps = roadmaps[roadmap_idx]["steps"]
        if not steps:
            print("This roadmap has no steps yet.")
            return
        print("\nSelect a step to edit:")
        for i, step in enumerate(steps, start=1):
            print(f"{i}. {step['title']}")
        while True:
            step_num = input("Enter step number: ").strip()
            if step_num.isdigit() and 1 <= int(step_num) <= len(steps):
                step_idx = int(step_num) - 1
                break
            print("Invalid input. Please try again.")
        new_step_title = input("Enter new step title: ").strip()
        if new_step_title:
            old_step_title = steps[step_idx]["title"]
            steps[step_idx]["title"] = new_step_title
            save_data(data)
            print(f"Step title changed from '{old_step_title}' to '{new_step_title}'.")
        else:
            print("Step title cannot be empty.")

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
        # console.print("[bold white]Select a step [/]", justify='center')
       
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
