import json
import rich
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from rich import box
import matplotlib.pyplot as plt
import numpy as np
# notes :
# ill use rich
# ill add things like “Are you sure you want to delete ‘Learn Python’?”
# ill edit the indexing to all to be 1 based
# ill edit minor issues
def  load_data():
    try : 
        with open("data.json" ,"r") as f : 
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
             data = {
            "categories": ["Programming", "Design", "Languages", "Business", "Other"],
            "roadmaps": []
        }
    return data



def save_data(data) :
          with open ("data.json" , "w") as f :
                 json.dump(data, f, indent=4)

def create_roadmap(data):
    print("[Create Roadmap]")
    
    # Show available categories
    print("\nAvailable categories:")
    for i, category in enumerate(data["categories"], start=1):
        print(f"{i}. {category}")
    print(f"{len(data['categories']) + 1}. Add new category")
    
    # Get category choice
    while True:
        cat_choice = input("\nSelect category number: ").strip()
        if cat_choice.isdigit():
            cat_choice = int(cat_choice)
            if 1 <= cat_choice <= len(data["categories"]) + 1:
                break
        print("Invalid input. Please try again.")
    
    # Handle category selection
    if cat_choice == len(data["categories"]) + 1:
        # Add new category
        new_category = input("Enter new category name: ").strip()
        if new_category:
            data["categories"].append(new_category)
            category = new_category
            print(f"Category '{new_category}' added.")
        else:
            category = "Other"
    else:
        category = data["categories"][cat_choice - 1]
    
    # Get roadmap title
    title = input("Enter title for the roadmap: ").strip()
    if title:
        data["roadmaps"].append({
            "title": title, 
            "category": category,
            "steps": []
        })
        save_data(data)
        print(f"Roadmap '{title}' created in category '{category}'.")

def manage_categories(data):
    print("\n[Manage Categories]")
    while True:
        print("\n1. View all categories")
        print("2. Add category")
        print("3. Delete category")
        print("4. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            view_categories(data)
        elif choice == "2":
            add_category(data)
        elif choice == "3":
            delete_category(data)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def view_categories(data):
    print("\n=== All Categories ===")
    if not data["categories"]:
        print("No categories found.")
        return
    
    for i, category in enumerate(data["categories"], start=1):
        # Count roadmaps in this category
        count = sum(1 for roadmap in data["roadmaps"] if roadmap.get("category") == category)
        print(f"{i}. {category} ({count} roadmaps)")
def add_category(data):
    print("\n[Add Category]")
    new_category = input("Enter new category name: ").strip()
    if new_category:
        if new_category in data["categories"]:
            print("Category already exists!")
        else:
            data["categories"].append(new_category)
            save_data(data)
            print(f"Category '{new_category}' added.")
    else:
        print("Category name cannot be empty.")
def delete_category(data):
    print("\n[Delete Category]")
    if not data["categories"]:
        print("No categories to delete.")
        return
    
    view_categories(data)
    
    while True:
        choice = input("\nEnter category number to delete (or 'c' to cancel): ").strip()
        if choice.lower() == 'c':
            return

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(data["categories"]):
                category = data["categories"][choice - 1]
                
                # Check if category is used by any roadmaps
                used_by = [r for r in data["roadmaps"] if r.get("category") == category]
                if used_by:
                    print(f"Cannot delete '{category}' - it's used by {len(used_by)} roadmap(s).")
                    print("Reassign or delete those roadmaps first.")
                    return
                confirm = input(f"Are you sure you want to delete '{category}'? (y/n): ").strip().lower()
                if confirm != "y":
                    print("Deletion canceled.")
                    return
                # Delete category
                data["categories"].pop(choice - 1)
                save_data(data)
                print(f"Category '{category}' deleted.")
                return
        print("Invalid input. Please try again.")
         
def view_roadmaps(data):
    print("\n[View Roadmaps]")

        # Option to filter by category
    print("View options:")
    print("1. View all roadmaps")
    print("2. View by category")
    
    choice = input("Select option: ").strip()
    
    if choice == "2":
        view_roadmaps_by_category(data)
    else:
        view_all_roadmaps(data)
def view_all_roadmaps(data):

    if not data["roadmaps"]:
        print("No roadmaps found.\n")
        return

    for roadmap in data["roadmaps"]:
        # Calculate progress percentage
        steps = roadmap.get("steps", [])
        total = len(steps)
        completed = sum(1 for step in steps if step.get("done", False))
        percent = (completed / total * 100) if total > 0 else 0
        
        # Display roadmap with progress
        print(f"\n=== Roadmap: {roadmap['title']} ({percent:.1f}% complete) ===\n")
        
        if steps:
            for i, step in enumerate(steps, start=1):
                status = "✓" if step.get("done", False) else "✗"
                print(f"  {i}. [{status}] {step['title']}")
        else:
            print("  (No steps yet)")
        print("=" * 40)
        print(f"Progress: {completed}/{total} steps completed")
        print("\n")

def add_step(data) :
      
      # select which task 
        print("\n[3] add step")

        roadmaps= data["roadmaps"]
        if not roadmaps:
                print("No roadmaps available.")
                return
        print("\nSelect a roadmap (or 'q' to quit):")
        for i, roadmap in enumerate(roadmaps, start=1):
                print(f"{i}. {roadmap['title']}")
        while True : 
                task = input("Enter roadmap number: ").strip()
                if task.lower() == "q":
                     return
                if task.isdigit() and 1 <= int(task) <= len(roadmaps):
                        idx = int(task) - 1
                        break
                print("Invalid input. Please try again.")
      # add a step to this task 
        step_title = input("Enter step title: ").strip()
        if step_title:
          roadmaps[idx]["steps"].append({"title": step_title, "done": False})
          save_data(data)
          print(f"Step '{step_title}' added to '{roadmaps[idx]['title']}'.")


def mark_step_complete(data) :
        print("\n[4] Mark Step Complete")
      # select which task 
        roadmaps= data["roadmaps"]
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
        while True :
              step_num = input("Enter step number : ")
              if step_num.isdigit() : 
                    idxS = int(step_num)
                    if 1 <= idxS <= len(steps):
                          idxS = idxS - 1  # Convert to 0-based for internal use
                          break
              print("Invalid input. Please enter a valid number.")
        # safe the updated data
        steps[idxS]["done"] = not steps[idxS]["done"]
        state = "complete" if steps[idxS]["done"] else "incomplete"
        save_data(data)
        print(f"Step '{steps[idxS]['title']}' marked as {state}")


def view_progress(data):
    print("\n[View Progress]")
    percent = 0
    if not data["roadmaps"]:
        print("No roadmaps found.")
        return
    for roadmap in data["roadmaps"]:
        steps = roadmap["steps"]
        total = len(steps)
        completed = sum(1 for step in steps if step["done"])
        percent = (completed / total * 100) if total > 0 else 0
        print(f"\nRoadmap: {roadmap['title']} {percent:.1f}%")
        print(f"Progress: {completed}/{total} steps completed {percent:.1f}%")
    
def Sort_Roadmaps(data):
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

def view_roadmaps_by_category(data):
    if not data["categories"]:
        print("No categories available.")
        return
    
    print("\nSelect category:")
    for i, category in enumerate(data["categories"], start=1):
        count = sum(1 for roadmap in data["roadmaps"] if roadmap.get("category") == category)
        print(f"{i}. {category} ({count} roadmaps)")
    
    while True:
        choice = input("Enter category number: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(data["categories"]):
                category = data["categories"][choice - 1]
                break
        print("Invalid input. Please try again.")
    
    # Filter roadmaps by category
    category_roadmaps = [r for r in data["roadmaps"] if r.get("category") == category]
    
    if not category_roadmaps:
        print(f"No roadmaps found in category '{category}'.")
        return
    
    print(f"\n=== {category} Roadmaps ===")
    for roadmap in category_roadmaps:
        steps = roadmap.get("steps", [])
        total = len(steps)
        completed = sum(1 for step in steps if step.get("done", False))
        percent = (completed / total * 100) if total > 0 else 0
        
        print(f"\n• {roadmap['title']} ({percent:.1f}% complete)")
def Categories(data):
    console = Console()
    console.print("\n[bold][Category Progress][/bold]")
    if not data["categories"]:
        console.print("[red]No categories found.[/red]")
        return
    
    table = Table(title="Category Progress", show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan")
    table.add_column("Roadmaps", justify="center")
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
    total_steps = sum(len(roadmap["steps"]) for roadmap in data["roadmaps"])
    completed_steps = sum(sum(1 for step in roadmap["steps"] if step["done"]) for roadmap in data["roadmaps"])
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
    
    # Display each roadmap with beautiful progress visualization
    for roadmap in data["roadmaps"]:
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
        
        # Create beautiful progress bar with gradient
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
                    completed_steps_list.add_row(f"   🟢 {step['title']}")
        
        # Pending steps list (if any)
        if completed < total:
            pending_steps_list = Table(show_header=False, box=None)
            pending_steps_list.add_row("[yellow]⏳ Pending:[/yellow]")
            for step in steps:
                if not step["done"]:
                    pending_steps_list.add_row(f"   🔴 {step['title']}")
        
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
    motivational_msg = get_motivational_message(overall_percent)
    console.print(Panel.fit(f"💪 [italic]{motivational_msg}[/italic]", 
                          border_style="yellow", box=box.ROUNDED))
    
    # Add quick tips
    console.print("\n[dim]💡 Tips: Use '[white]4[/white]' to mark steps complete • '[white]7[/white]' to sort roadmaps • '[white]8[/white]' to manage categories[/dim]")

def get_motivational_message(percent):
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

# Optional: Add a loading animation for extra polish
def show_loading_animation():
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
            import time
            time.sleep(0.02)
def import_export(data)  :
     print(f"\n[Import/Export Roadmaps]")
     print("1. Export roadmap")
     print("2. Import roadmap")
     choice = input("Select option: ").strip()
     if choice.isdigit():
            choice = int(choice)
            if choice >= 1 or choice <= 2:
                 return
            print("number must be between 1 and 2")
     if choice == 1 :
        if not data["roadmaps"] :
             print ("No roadmaps to export")
             return
        for i , roadmap in enumerate (data["roadmaps"], start=1) :
             print (f"{i}. {roadmap['title']}")
        while True : 
             idx = input("Enter roadmap number").strip()
             if idx.isdigit() and 1 <= int(idx) <= len(data['roadmaps']):
                  idx= int(idx) - 1
                  break
             print ("Invalid input")
        filename = input(f"Enter export filename (e.g , roadmap.json): ").strip()
        try : 
         with open (filename , "w") as f :
             json.dump(data["roadmaps"][idx],f, indent=4)
             print(f"Roadmap exported to '{filename}'.")
        except IOError as e:
            print(f"Error writing to file: {e}")
     elif choice == "2":
        filename = input("Enter import filename: ").strip()
        try:
            with open(filename, "r") as f:
                roadmap = json.load(f)
            data["roadmaps"].append(roadmap)
            save_data(data)
            print(f"Roadmap '{roadmap['title']}' imported.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Invalid file or JSON format.")
    

def edit(data):
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
        
def delete(data):
         
        print("\n[5] Delete Roadmap/Step")
        while True:
         oper = input("Enter 1 to delete a roadmap, 2 to delete a step: ").strip()
         if oper.isdigit():
               oper = int(oper)
               if 1 <= oper <= 2:
                  break
         print("Invalid input. Please enter a valid number.")
         
         
        roadmaps = data["roadmaps"]
        if not roadmaps:
          print("No roadmaps available.")
          return
        
        print("\n=== Select a roadmap by typing its number ===")

        for i in range (len(roadmaps)) :
              print(f"{i+1}. {roadmaps[i]['title']}")

        while True :
             roadmap_idx = input("Enter roadmap Number : ")
             if roadmap_idx.isdigit():
               roadmap_idx = int(roadmap_idx)
               if 1 <= roadmap_idx <= len(roadmaps):
                  roadmap_idx = roadmap_idx - 1  # Convert to 0-based for internal use
                  break
             print("Invalid input. Please enter a valid number.")
        if oper == 1:  
             confirm = input(f"Are you sure you want to delete '{roadmaps[roadmap_idx]['title']}'? (y/n): ").strip().lower()
             if confirm != "y":
                  print("Deletion canceled.")
                  return
             deleted = roadmaps.pop(roadmap_idx)
             save_data(data)
             print(f"Roadmap '{deleted['title']}' deleted.")

        elif oper == 2 :
             
             steps = roadmaps[roadmap_idx]["steps"]
             if not steps:
                print("This roadmap has no steps yet.")
                return
             print("\n=== Select a step to delete by typing its number ===")
             for i in range (len(steps)) :
                  print(f"{i+1}. {steps[i]['title']}")
             while True : 
                  step_num = input("Enter step num : ")
                  if step_num.isdigit() : 
                        idxS = int(step_num)
                        if 1 <= idxS <= len(steps):
                           idxS = idxS - 1  # Convert to 0-based for internal use
                           break
                  print("Invalid input. Please enter a valid number.")
             deleted = steps.pop(idxS)
             save_data(data)
             print(f"Step '{deleted['title']}' deleted from roadmap '{roadmaps[roadmap_idx]['title']}'.")
        else :    
             print("Invalid choice. Please enter 1 or 2.")
def main():
    data = load_data()
    while True:
        print("""
=============================
 Learning Roadmap Builder
=============================
[1] View Roadmaps
[2] Create Roadmap
[3] Add Step
[4] Mark Step Complete
[5] Delete Roadmap/Step
[6] View Progress
[7] Sort Roadmaps
[8] Manage Categories
[9] Category Overview
[10] Progress Visualization
[11] Edit Roadmap/Step
[12] Import/Export Roadmaps
[13] Exit
""")
        
        choice = input("Select an option: ").strip()
        if choice.isdigit():
            idx = int(choice)
            match idx:
                case 1:
                    view_roadmaps(data)
                    input("Press Enter to continue...")
                case 2:
                    create_roadmap(data)
                    input("Press Enter to continue...")
                case 3:
                    add_step(data)
                    input("Press Enter to continue...")
                case 4:
                    mark_step_complete(data)
                    input("Press Enter to continue...")
                case 5:
                    delete(data)
                    input("Press Enter to continue...")
                case 6:
                    view_progress(data)
                    input("Press Enter to continue...")
                case 7:
                    Sort_Roadmaps(data)
                    input("Press Enter to continue...")
                case 8:
                    manage_categories(data)
                case 9:
                    Categories(data)
                    input("Press Enter to continue...")
                case 10:
                    Progress_Visualization(data)
                    input("Press Enter to continue...")
                case 11:
                    edit(data)
                    input("Press Enter to continue...")
                case 12:
                    import_export(data)
                    input("Press Enter to continue...")
                case 13:
                    print("Exiting.......")
                    break
                case _: 
                    print("Invalid choice. Please select a number between 1 and 13.")
        else:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()