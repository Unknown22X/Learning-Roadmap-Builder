# import json
# import rich
# from rich.console import Console
# from rich.progress import Progress, BarColumn, TextColumn
# from rich.panel import Panel
# from rich.table import Table
# from rich import box
# import time
# from rich.text import Text
# from rich.align import Align
# from rich.columns import Columns
# # notes :
# # ill use rich
# def load_data():
#     try : 
#         with open("data.json" ,"r") as f : 
#             data = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#              data = {
#             "categories": ["Programming", "Design", "Languages", "Business", "Other"],
#             "roadmaps": []
#         }
#     return data



# def save_data(data) :
#           with open ("data.json" , "w") as f :
#                  json.dump(data, f, indent=4)

# def create_roadmap(data):
#     print("[Create Roadmap]")
    
#     # Show available categories
#     print("\nAvailable categories:")
#     for i, category in enumerate(data["categories"], start=1):
#         print(f"{i}. {category}")
#     print(f"{len(data['categories']) + 1}. Add new category")
    
#     # Get category choice
#     while True:
#         cat_choice = input("\nSelect category number: ").strip()
#         if cat_choice.isdigit():
#             cat_choice = int(cat_choice)
#             if 1 <= cat_choice <= len(data["categories"]) + 1:
#                 break
#         print("Invalid input. Please try again.")
    
#     # Handle category selection
#     if cat_choice == len(data["categories"]) + 1:
#         # Add new category
#         new_category = input("Enter new category name: ").strip()
#         if new_category:
#             data["categories"].append(new_category)
#             category = new_category
#             print(f"Category '{new_category}' added.")
#         else:
#             category = "Other"
#     else:
#         category = data["categories"][cat_choice - 1]
    
#     # Get roadmap title
#     title = input("Enter title for the roadmap: ").strip()
#     if not title or title.isspace():
#         print("Title cannot be empty or just spaces.")
#         return
#     if title:
#         data["roadmaps"].append({
#             "title": title, 
#             "category": category,
#             "steps": []
#         })
#         save_data(data)
#         print(f"Roadmap '{title}' created in category '{category}'.")

# def manage_categories(data):
#     print("\n[Manage Categories]")
#     while True:
#         print("\n1. View all categories")
#         print("2. Add category")
#         print("3. Delete category")
#         print("4. Back to main menu")
        
#         choice = input("Select option: ").strip()
        
#         if choice == "1":
#             view_categories(data)
#         elif choice == "2":
#             add_category(data)
#         elif choice == "3":
#             delete_category(data)
#         elif choice == "4":
#             break
#         else:
#             print("Invalid choice. Please try again.")

# def view_categories(data):
#     print("\n=== All Categories ===")
#     if not data["categories"]:
#         print("No categories found.")
#         return
    
#     for i, category in enumerate(data["categories"], start=1):
#         # Count roadmaps in this category
#         count = sum(1 for roadmap in data["roadmaps"] if roadmap.get("category") == category)
#         print(f"{i}. {category} ({count} roadmaps)")
# def add_category(data):
#     print("\n[Add Category]")
#     new_category = input("Enter new category name: ").strip()
#     if new_category:
#         if new_category in data["categories"]:
#             print("Category already exists!")
#         else:
#             data["categories"].append(new_category)
#             save_data(data)
#             print(f"Category '{new_category}' added.")
#     else:
#         print("Category name cannot be empty.")
# def delete_category(data):
#     print("\n[Delete Category]")
#     if not data["categories"]:
#         print("No categories to delete.")
#         return
    
#     view_categories(data)
    
#     while True:
#         choice = input("\nEnter category number to delete (or 'c' to cancel): ").strip()
#         if choice.lower() == 'c':
#             return

#         if choice.isdigit():
#             choice = int(choice)
#             if 1 <= choice <= len(data["categories"]):
#                 category = data["categories"][choice - 1]
                
#                 # Check if category is used by any roadmaps
#                 used_by = [r for r in data["roadmaps"] if r.get("category") == category]
#                 if used_by:
#                     print(f"Cannot delete '{category}' - it's used by {len(used_by)} roadmap(s).")
#                     print("Reassign or delete those roadmaps first.")
#                     return
#                 confirm = input(f"Are you sure you want to delete '{category}'? (y/n): ").strip().lower()
#                 if confirm != "y":
#                     print("Deletion canceled.")
#                     return
#                 # Delete category
#                 data["categories"].pop(choice - 1)
#                 save_data(data)
#                 print(f"Category '{category}' deleted.")
#                 return
#         print("Invalid input. Please try again.")
         
# def view_roadmaps(data):
#     print("\n[View Roadmaps]")

#         # Option to filter by category
#     print("View options:")
#     print("1. View all roadmaps")
#     print("2. View by category")
    
#     choice = input("Select option: ").strip()
    
#     if choice == "2":
#         view_roadmaps_by_category(data)
#     else:
#         view_all_roadmaps(data)
# def view_all_roadmaps(data):

#     if not data["roadmaps"]:
#         print("No roadmaps found.\n")
#         return

#     for roadmap in data["roadmaps"]:
#         # Calculate progress percentage
#         steps = roadmap.get("steps", [])
#         total = len(steps)
#         completed = sum(1 for step in steps if step.get("done", False))
#         percent = (completed / total * 100) if total > 0 else 0
        
#         # Display roadmap with progress
#         print(f"\n=== Roadmap: {roadmap['title']} ({percent:.1f}% complete) ===\n")
        
#         if steps:
#             for i, step in enumerate(steps, start=1):
#                 status = "✓" if step.get("done", False) else "✗"
#                 print(f"  {i}. [{status}] {step['title']}")
#         else:
#             print("  (No steps yet)")
#         print("=" * 40)
#         print(f"Progress: {completed}/{total} steps completed")
#         print("\n")

# def add_step(data) :
      
#       # select which task 
#         print("\n[3] add step")

#         roadmaps= data["roadmaps"]
#         if not roadmaps:
#                 print("No roadmaps available.")
#                 return
#         print("\nSelect a roadmap (or 'q' to quit):")
#         for i, roadmap in enumerate(roadmaps, start=1):
#                 print(f"{i}. {roadmap['title']}")
#         while True : 
#                 task = input("Enter roadmap number: ").strip()
#                 if task.lower() == "q":
#                      return
#                 if task.isdigit() and 1 <= int(task) <= len(roadmaps):
#                         idx = int(task) - 1
#                         break
#                 print("Invalid input. Please try again.")
#       # add a step to this task 

#         step_title = input("Enter step title: ").strip()
#         if not step_title:
#             print("Step title cannot be empty.")
#             return
#         if step_title:
#           roadmaps[idx]["steps"].append({"title": step_title, "done": False})
#           save_data(data)
#           print(f"Step '{step_title}' added to '{roadmaps[idx]['title']}'.")


# def mark_step_complete(data) :
#         print("\n[4] Mark Step Complete")
#       # select which task 
#         roadmaps= data["roadmaps"]
#         if not roadmaps:
#                 print("No roadmaps available.")
#                 return
#         print("\n=== Select a roadmap by typing its number : \n")
#         for i, roadmap in enumerate(roadmaps, start=1):
#          print(f"{i}. {roadmap['title']}")
#         while True:
#             task = input("Enter roadmap number: ").strip()
#             if task.isdigit() and 1 <= int(task) <= len(roadmaps):
#                  idx = int(task) - 1
#                  break
#             print("Invalid input. Please enter a valid number.")

#         # select which step : 
#         steps = roadmaps[idx]["steps"]
#         if not steps:
#          print("This roadmap has no steps yet.")
#          return

#         print("\n=== Select a step by typing its number : \n")
#         for i, step in enumerate(steps, start=1):
#             print(f"{i}. {step['title']}")
#         while True :
#               step_num = input("Enter step number : ")
#               if step_num.isdigit() : 
#                     idxS = int(step_num)
#                     if 1 <= idxS <= len(steps):
#                           idxS = idxS - 1  # Convert to 0-based for internal use
#                           break
#               print("Invalid input. Please enter a valid number.")
#         # safe the updated data
#         steps[idxS]["done"] = not steps[idxS]["done"]
#         state = "complete" if steps[idxS]["done"] else "incomplete"
#         save_data(data)
#         print(f"Step '{steps[idxS]['title']}' marked as {state}")


# def view_progress(data):
#     print("\n[View Progress]")
#     percent = 0
#     if not data["roadmaps"]:
#         print("No roadmaps found.")
#         return
#     for roadmap in data["roadmaps"]:
#         steps = roadmap["steps"]
#         total = len(steps)
#         completed = sum(1 for step in steps if step["done"])
#         percent = (completed / total * 100) if total > 0 else 0
#         print(f"\nRoadmap: {roadmap['title']} {percent:.1f}%")
#         print(f"Progress: {completed}/{total} steps completed {percent:.1f}%")
    
# def Sort_Roadmaps(data):
#     print("\n[Sort Roadmaps]")
#     if not data["roadmaps"]:
#         print("No roadmaps to sort.")
#         return
#     print("1. Sort by title\n2. Sort by progress\n3. Sort by category")
#     choice = input("Select option: ").strip()
#     if choice == "1":
#         data["roadmaps"].sort(key=lambda x: x["title"].lower())
#     elif choice == "2":
#         data["roadmaps"].sort(key=lambda x: sum(1 for s in x["steps"] if s["done"]) / len(x["steps"]) if x["steps"] else 0, reverse=True)
#     elif choice == "3":
#         data["roadmaps"].sort(key=lambda x: x.get("category", "Uncategorized"))
#     save_data(data)
#     print("Roadmaps sorted.")

# def view_roadmaps_by_category(data):
#     if not data["categories"]:
#         print("No categories available.")
#         return
    
#     print("\nSelect category:")
#     for i, category in enumerate(data["categories"], start=1):
#         count = sum(1 for roadmap in data["roadmaps"] if roadmap.get("category") == category)
#         print(f"{i}. {category} ({count} roadmaps)")
    
#     while True:
#         choice = input("Enter category number: ").strip()
#         if choice.isdigit():
#             choice = int(choice)
#             if 1 <= choice <= len(data["categories"]):
#                 category = data["categories"][choice - 1]
#                 break
#         print("Invalid input. Please try again.")
    
#     # Filter roadmaps by category
#     category_roadmaps = [r for r in data["roadmaps"] if r.get("category") == category]
    
#     if not category_roadmaps:
#         print(f"No roadmaps found in category '{category}'.")
#         return
    
#     print(f"\n=== {category} Roadmaps ===")
#     for roadmap in category_roadmaps:
#         steps = roadmap.get("steps", [])
#         total = len(steps)
#         completed = sum(1 for step in steps if step.get("done", False))
#         percent = (completed / total * 100) if total > 0 else 0
        
#         print(f"\n• {roadmap['title']} ({percent:.1f}% complete)")
# def Categories(data):
#     console = Console()
#     console.print("\n[bold][Category Progress][/]")
#     if not data["categories"]:
#         console.print("[red]No categories found.[/]")
#         return
    
#     table = Table(title="Category Progress", show_header=True, header_style="bold magenta")
#     table.add_column("Category", style="cyan" , justify="center")
#     table.add_column("Roadmaps")
#     table.add_column("Steps Completed", justify="center")
#     table.add_column("Progress", justify="center")
    
#     for category in data["categories"]:
#         roadmaps = [r for r in data["roadmaps"] if r.get("category") == category]
#         total_roadmaps = len(roadmaps)
#         total_steps = sum(len(r["steps"]) for r in roadmaps)
#         completed_steps = sum(sum(1 for s in r["steps"] if s["done"]) for r in roadmaps)
#         percent = (completed_steps / total_steps * 100) if total_steps > 0 else 0
#         table.add_row(category, str(total_roadmaps), f"{completed_steps}/{total_steps}", f"{percent:.1f}%")
    
#     console.print(table)

# def Progress_Visualization(data):
#     console = Console()
    
#     # Clear screen and create a beautiful header
#     console.clear()
#     console.print(Panel.fit("🎯 [bold cyan]Learning Progress Dashboard[/bold cyan] 🎯", 
#                           style="bold blue", subtitle="Track your learning journey"))
    
#     if not data["roadmaps"]:
#         console.print("\n[italic yellow]No roadmaps found. Create your first roadmap to start tracking progress![/italic yellow]")
#         console.print("\n💡 [dim]Tip: Use option 2 to create a new roadmap[/dim]")
#         return
    
#     # Create overall statistics
#     total_roadmaps = len(data["roadmaps"])
#     total_steps = sum(len(roadmap["steps"]) for roadmap in data["roadmaps"])
#     completed_steps = sum(sum(1 for step in roadmap["steps"] if step["done"]) for roadmap in data["roadmaps"])
#     overall_percent = (completed_steps / total_steps * 100) if total_steps > 0 else 0
    
#     # Overall progress panel
#     overall_panel = Panel(
#         f"""📊 [bold]Overall Progress:[/bold] [green]{overall_percent:.1f}%[/green]
        
# ├─ 🗺️  Roadmaps: [cyan]{total_roadmaps}[/cyan]
# ├─ 📝 Total Steps: [white]{total_steps}[/white]
# ├─ ✅ Completed: [green]{completed_steps}[/green]
# └─ ⏳ Remaining: [yellow]{total_steps - completed_steps}[/yellow]""",
#         title="📈 Overall Statistics",
#         border_style="cyan",
#         box=box.ROUNDED
#     )
    
#     console.print(overall_panel)
#     console.print()  # Spacer
    
#     # Display each roadmap  
#     for roadmap in data["roadmaps"]:
#         steps = roadmap["steps"]
#         total = len(steps)
#         completed = sum(1 for step in steps if step["done"])
#         percent = (completed / total * 100) if total > 0 else 0
        
#         # Determine status and colors
#         if percent == 0:
#             status_emoji, status_color, status_msg = "💤", "red", "Not started"
#         elif percent < 25:
#             status_emoji, status_color, status_msg = "🌱", "yellow", "Beginning"
#         elif percent < 50:
#             status_emoji, status_color, status_msg = "🚶‍♂️", "blue", "Progressing"
#         elif percent < 75:
#             status_emoji, status_color, status_msg = "🚀", "green", "Good pace!"
#         elif percent < 100:
#             status_emoji, status_color, status_msg = "🔥", "bright_green", "Almost there!"
#         else:
#             status_emoji, status_color, status_msg = "🎉", "bold green", "Completed!"
        
#         # Create  progress bar with gradient
#         bar_width = 30
#         filled_segments = int(bar_width * percent / 100)
#         progress_bar = ""
        
#         # Create gradient effect
#         for i in range(bar_width):
#             if i < filled_segments:
#                 # Gradient from green to bright green
#                 if i < filled_segments * 0.3:
#                     color = "green"
#                 elif i < filled_segments * 0.6:
#                     color = "bright_green"
#                 else:
#                     color = "bold green"
#                 progress_bar += f"[{color}]█[/{color}]"
#             else:
#                 progress_bar += "[dim]░[/dim]"
        
#         # Create the main content table
#         content_table = Table.grid()
#         content_table.add_column(width=35)
#         content_table.add_column(width=50)
        
#         # Progress bar and stats
#         progress_section = Table(show_header=False, box=None, show_lines=True)
#         progress_section.add_row(f"{status_emoji} [bold]{roadmap['title']}[/bold]")
#         progress_section.add_row(f"{progress_bar} [bold {status_color}]{percent:.1f}%[/bold {status_color}]")
#         progress_section.add_row(f"📊 [dim]{completed}/{total}[/dim] steps • 🎯 [dim]{status_msg}[/dim]")
        
#         # Completed steps list (if any)
#         if completed > 0:
#             completed_steps_list = Table(show_header=False, box=None)
#             completed_steps_list.add_row("[green]✅ Completed:[/green]")
#             for step in steps:
#                 if step["done"]:
#                     completed_steps_list.add_row(f"   🟢 {step['title']}")
        
#         # Pending steps list (if any)
#         if completed < total:
#             pending_steps_list = Table(show_header=False, box=None)
#             pending_steps_list.add_row("[yellow]⏳ Pending:[/yellow]")
#             for step in steps:
#                 if not step["done"]:
#                     pending_steps_list.add_row(f"   🔴 {step['title']}")
        
#         # Combine everything
#         content_table.add_row(progress_section)
        
#         if completed > 0:
#             content_table.add_row(completed_steps_list)
#         if completed < total:
#             content_table.add_row(pending_steps_list)
        
#         # Create the panel
#         roadmap_panel = Panel(
#             content_table,
#             title=f"[bold]📋 {roadmap['title']}[/bold]",
#             subtitle=f"[dim]{len(steps)} steps[/dim]",
#             border_style=status_color,
#             box=box.ROUNDED,
#             padding=(1, 2)
#         )
        
#         console.print(roadmap_panel)
#         console.print()  # Spacer
    
#     # Add motivational message based on overall progress
#     motivational_msg = get_motivational_message(overall_percent)
#     console.print(Panel.fit(f"💪 [italic]{motivational_msg}[/italic]", 
#                           border_style="yellow", box=box.ROUNDED))
    
#     # Add quick tips
#     console.print("\n[dim]💡 Tips: Use '[white]4[/white]' to mark steps complete • '[white]7[/white]' to sort roadmaps • '[white]8[/white]' to manage categories[/dim]")

# def get_motivational_message(percent):
#     if percent == 0:
#         return "Every expert was once a beginner. Start your journey today! 🚀"
#     elif percent < 25:
#         return "Great start! Consistency is key. Keep going! 🌟"
#     elif percent < 50:
#         return "You're making solid progress! The middle is where champions are made. 💪"
#     elif percent < 75:
#         return "Wow! You're cruising now. Don't stop when you're tired, stop when you're done! 🔥"
#     elif percent < 100:
#         return "Almost there! The finish line is in sight. One final push! 🏁"
#     else:
#         return "Incredible! You've completed everything. Time to celebrate and set new goals! 🎊"

# def show_loading_animation():
#     console = Console()
#     with Progress(
#         TextColumn("[bold blue]Loading your progress[/bold blue]"),
#         BarColumn(bar_width=40),
#         TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
#         transient=True,
#     ) as progress:
#         task = progress.add_task("", total=100)
#         for i in range(100):
#             progress.update(task, advance=1)
#             import time
#             time.sleep(0.02)
# def import_export(data)  :
#      print(f"\n[Import/Export Roadmaps]")
#      print("1. Export roadmap")
#      print("2. Import roadmap")
#      choice = input("Select option: ").strip()
#      if choice.isdigit():
#         choice = int(choice)
#         if choice not in [1, 2]:
#          print("Number must be 1 or 2.")
#          return
#      else:
#          print("Invalid input. Please enter a number.")
#          return
#      if choice == 1 :
#         if not data["roadmaps"] :
#              print ("No roadmaps to export")
#              return
#         for i , roadmap in enumerate (data["roadmaps"], start=1) :
#              print (f"{i}. {roadmap['title']}")
#         while True : 
#              idx = input("Enter roadmap number").strip()
#              if idx.isdigit() and 1 <= int(idx) <= len(data['roadmaps']):
#                   idx= int(idx) - 1
#                   break
#              print ("Invalid input")
#         filename = input(f"Enter export filename (e.g , roadmap.json): ").strip()
#         try : 
#          with open (filename , "w") as f :
#              json.dump(data["roadmaps"][idx],f, indent=4)
#              print(f"Roadmap exported to '{filename}'.")
#         except IOError as e:
#             print(f"Error writing to file: {e}")
#      elif choice == "2":
#         filename = input("Enter import filename: ").strip()
#         try:
#             with open(filename, "r") as f:
#                 roadmap = json.load(f)
#             data["roadmaps"].append(roadmap)
#             save_data(data)
#             print(f"Roadmap '{roadmap['title']}' imported.")
#         except (FileNotFoundError, json.JSONDecodeError):
#             print("Error: Invalid file or JSON format.")
    

# def edit(data):
#         print("\n[Edit Roadmap/Step]")
#         roadmaps = data["roadmaps"]
#         if not roadmaps:
#                 print("No roadmaps available.")
#                 return

#         print("\nSelect a roadmap to edit:")
#         for i, roadmap in enumerate(roadmaps, start=1):
#                 print(f"{i}. {roadmap['title']}")
#         while True:
#                 roadmap_num = input("Enter roadmap number (or 'q' to quit): ").strip()
#                 if roadmap_num.lower() == "q":
#                         return
#                 if roadmap_num.isdigit() and 1 <= int(roadmap_num) <= len(roadmaps):
#                         roadmap_idx = int(roadmap_num) - 1
#                         break
#                 print("Invalid input. Please try again.")

#         print("\nEdit options:")
#         print("1. Edit roadmap title")
#         print("2. Edit step title")
#         while True:
#                 option = input("Select option: ").strip()
#                 if option in ("1", "2"):
#                         break
#                 print("Invalid input. Please enter 1 or 2.")

#         if option == "1":
#                 new_title = input("Enter new roadmap title: ").strip()
#                 if new_title:
#                         old_title = roadmaps[roadmap_idx]["title"]
#                         roadmaps[roadmap_idx]["title"] = new_title
#                         save_data(data)
#                         print(f"Roadmap title changed from '{old_title}' to '{new_title}'.")
#                 else:
#                         print("Title cannot be empty.")
#         else:
#                 steps = roadmaps[roadmap_idx]["steps"]
#                 if not steps:
#                         print("This roadmap has no steps yet.")
#                         return
#                 print("\nSelect a step to edit:")
#                 for i, step in enumerate(steps, start=1):
#                         print(f"{i}. {step['title']}")
#                 while True:
#                         step_num = input("Enter step number: ").strip()
#                         if step_num.isdigit() and 1 <= int(step_num) <= len(steps):
#                                 step_idx = int(step_num) - 1
#                                 break
#                         print("Invalid input. Please try again.")
#                 new_step_title = input("Enter new step title: ").strip()
#                 if new_step_title:
#                         old_step_title = steps[step_idx]["title"]
#                         steps[step_idx]["title"] = new_step_title
#                         save_data(data)
#                         print(f"Step title changed from '{old_step_title}' to '{new_step_title}'.")
#                 else:
#                         print("Step title cannot be empty.")
        
# def delete(data):
         
#         print("\n[5] Delete Roadmap/Step")
#         while True:
#          oper = input("Enter 1 to delete a roadmap, 2 to delete a step: ").strip()
#          if oper.isdigit():
#                oper = int(oper)
#                if 1 <= oper <= 2:
#                   break
#          print("Invalid input. Please enter a valid number.")
         
         
#         roadmaps = data["roadmaps"]
#         if not roadmaps:
#           print("No roadmaps available.")
#           return
        
#         print("\n=== Select a roadmap by typing its number ===")

#         for i, step in enumerate(steps, start=1):
#              print(f"{i}. {step['title']}")

#         while True :
#              roadmap_idx = input("Enter roadmap Number : ")
#              if roadmap_idx.isdigit():
#                roadmap_idx = int(roadmap_idx)
#                if 1 <= roadmap_idx <= len(roadmaps):
#                   roadmap_idx = roadmap_idx - 1  # Convert to 0-based for internal use
#                   break
#              print("Invalid input. Please enter a valid number.")
#         if oper == 1:  
#              confirm = input(f"Are you sure you want to delete '{roadmaps[roadmap_idx]['title']}'? (y/n): ").strip().lower()
#              if confirm != "y":
#                   print("Deletion canceled.")
#                   return
#              deleted = roadmaps.pop(roadmap_idx)
#              save_data(data)
#              print(f"Roadmap '{deleted['title']}' deleted.")

#         elif oper == 2 :
             
#              steps = roadmaps[roadmap_idx]["steps"]
#              if not steps:
#                 print("This roadmap has no steps yet.")
#                 return
#              print("\n=== Select a step to delete by typing its number ===")
#              for i in range (len(steps)) :
#                   print(f"{i+1}. {steps[i]['title']}")
#              while True : 
#                   step_num = input("Enter step num : ")
#                   if step_num.isdigit() : 
#                         idxS = int(step_num)
#                         if 1 <= idxS <= len(steps):
#                            idxS = idxS - 1  # Convert to 0-based for internal use
#                            break
#                   print("Invalid input. Please enter a valid number.")
#              confirm = input(f"Are you sure you want to delete '{steps[idxS]['title']}'? (y/n): ").strip().lower()
#              if confirm != "y":
#                   print("Deletion canceled.")
#                   return
#              deleted = steps.pop(idxS)
#              save_data(data)
#              print(f"Step '{deleted['title']}' deleted from roadmap '{roadmaps[roadmap_idx]['title']}'.")
        


# def show_welcome_animation():
#     """Display an animated welcome screen"""
#     console = Console()
#     console.clear()
    
#     # Animated title
#     title_frames = [
#         "🎯 Learning Roadmap Builder",
#         "🎯 Learning Roadmap Builder ✨",
#         "🎯 Learning Roadmap Builder ✨🚀",
#         "🎯 Learning Roadmap Builder ✨🚀💡"
#     ]
    
#     for frame in title_frames:
#         console.clear()
#         console.print(Panel.fit(
#             f"[bold bright_blue]{frame}[/bold bright_blue]",
#             border_style="bright_blue",
#             box=box.DOUBLE
#         ), justify="center")
#         time.sleep(0.3)
    
#     # Welcome message
#     welcome_text = Text()
#     welcome_text.append("Welcome to your personal learning companion! ", style="bright_cyan")
#     welcome_text.append("🌟", style="yellow")
    
#     console.print()
#     console.print(Align.center(welcome_text))
#     console.print()
#     time.sleep(1)

# def create_menu_panel():
#     """Create a beautiful menu using Rich components"""
#     console = Console()
    
#     # Create menu sections
#     view_section = Table(show_header=False, box=None, padding=(0, 1))
#     view_section.add_row("📋 [bold cyan]1[/bold cyan] View Roadmaps", "Browse your learning paths")
#     view_section.add_row("📊 [bold cyan]6[/bold cyan] View Progress", "Check completion status") 
#     view_section.add_row("🎨 [bold cyan]10[/bold cyan] Progress Visualization", "Beautiful progress display")
    
#     manage_section = Table(show_header=False, box=None, padding=(0, 1))
#     manage_section.add_row("✨ [bold green]2[/bold green] Create Roadmap", "Start a new learning journey")
#     manage_section.add_row("➕ [bold green]3[/bold green] Add Step", "Add tasks to your roadmap")
#     manage_section.add_row("✅ [bold green]4[/bold green] Mark Step Complete", "Track your achievements")
#     manage_section.add_row("✏️  [bold green]11[/bold green] Edit Roadmap/Step", "Modify existing content")
    
#     organize_section = Table(show_header=False, box=None, padding=(0, 1))
#     organize_section.add_row("🗂️  [bold yellow]8[/bold yellow] Manage Categories", "Organize your topics")
#     organize_section.add_row("📈 [bold yellow]9[/bold yellow] Category Overview", "View category stats")
#     organize_section.add_row("🔄 [bold yellow]7[/bold yellow] Sort Roadmaps", "Organize your roadmaps")
    
#     tools_section = Table(show_header=False, box=None, padding=(0, 1))
#     tools_section.add_row("💾 [bold magenta]12[/bold magenta] Import/Export", "Backup & share roadmaps")
#     tools_section.add_row("🗑️  [bold red]5[/bold red] Delete Roadmap/Step", "Remove unwanted items")
#     tools_section.add_row("🚪 [bold white]13[/bold white] Exit", "Save and quit")
    
#     # Create panels for each section
#     view_panel = Panel(view_section, title="[bold bright_blue]📊 View & Track[/bold bright_blue]", 
#                       border_style="bright_blue", box=box.ROUNDED)
#     manage_panel = Panel(manage_section, title="[bold bright_green]🛠️  Create & Manage[/bold bright_green]", 
#                         border_style="bright_green", box=box.ROUNDED)
#     organize_panel = Panel(organize_section, title="[bold bright_yellow]🗂️  Organize[/bold bright_yellow]", 
#                           border_style="bright_yellow", box=box.ROUNDED)
#     tools_panel = Panel(tools_section, title="[bold bright_magenta]🔧 Tools & Utilities[/bold bright_magenta]", 
#                        border_style="bright_magenta", box=box.ROUNDED)
    
#     return [view_panel, manage_panel, organize_panel, tools_panel]

# def get_user_stats(data):
#     """Calculate and return user statistics"""
#     total_roadmaps = len(data["roadmaps"])
#     total_steps = sum(len(roadmap["steps"]) for roadmap in data["roadmaps"])
#     completed_steps = sum(sum(1 for step in roadmap["steps"] if step["done"]) 
#                          for roadmap in data["roadmaps"])
#     completion_rate = (completed_steps / total_steps * 100) if total_steps > 0 else 0
    
#     return {
#         "roadmaps": total_roadmaps,
#         "steps": total_steps,
#         "completed": completed_steps,
#         "completion_rate": completion_rate
#     }

# def create_stats_display(data):
#     """Create a beautiful stats display"""
#     stats = get_user_stats(data)
    
#     # Create stats table
#     stats_table = Table(show_header=False, box=None)
#     stats_table.add_column(justify="center", style="bold")
#     stats_table.add_column(justify="center")
    
#     # Determine progress emoji and color
#     rate = stats["completion_rate"]
#     if rate == 0:
#         progress_emoji, progress_color = "💤", "red"
#         progress_msg = "Ready to start!"
#     elif rate < 25:
#         progress_emoji, progress_color = "🌱", "yellow" 
#         progress_msg = "Getting started"
#     elif rate < 50:
#         progress_emoji, progress_color = "🚶‍♂️", "blue"
#         progress_msg = "Making progress"
#     elif rate < 75:
#         progress_emoji, progress_color = "🚀", "green"
#         progress_msg = "Great momentum!"
#     elif rate < 100:
#         progress_emoji, progress_color = "🔥", "bright_green"
#         progress_msg = "Almost there!"
#     else:
#         progress_emoji, progress_color = "🎉", "bold green"
#         progress_msg = "All completed!"
    
#     stats_table.add_row(f"{progress_emoji}", f"[{progress_color}]{rate:.1f}% Complete[/{progress_color}]")
#     stats_table.add_row("🗺️", f"[cyan]{stats['roadmaps']}[/cyan] Roadmaps")
#     stats_table.add_row("📝", f"[white]{stats['steps']}[/white] Total Steps")
#     stats_table.add_row("✅", f"[green]{stats['completed']}[/green] Completed")
    
#     return Panel(
#         Align.center(stats_table),
#         title=f"[bold]{progress_emoji} Your Progress[/bold]",
#         subtitle=f"[dim]{progress_msg}[/dim]",
#         border_style=progress_color,
#         box=box.ROUNDED
#     )

# def show_motivational_tip():
#     """Display a random motivational tip"""
#     tips = [
#         "💡 Break large goals into smaller, manageable steps!",
#         "🎯 Consistency beats perfection every time!",
#         "🌟 Every expert was once a beginner!",
#         "🚀 Progress, not perfection, is the goal!",
#         "💪 Small daily improvements lead to stunning results!",
#         "⭐ Your only competition is who you were yesterday!",
#         "🎨 Learning is a journey, not a destination!",
#         "🔥 The best time to start was yesterday, the second best time is now!",
#     ]
    
#     import random
#     tip = random.choice(tips)
    
#     return Panel.fit(
#         f"[italic bright_yellow]{tip}[/italic bright_yellow]",
#         border_style="yellow",
#         box=box.ROUNDED
#     )

# def main():
#     console = Console()
#     data = load_data()
    
#     # Show welcome animation on first run
#     show_welcome_animation()
    
#     while True:
#         console.clear()
        
#         # Create main header
#         header = Panel.fit(
#             "[bold bright_cyan]🎯 Learning Roadmap Builder 🎯[/bold bright_cyan]",
#             subtitle="[dim]Your Personal Learning Companion[/dim]",
#             border_style="bright_cyan",
#             box=box.DOUBLE
#         )
#         console.print(header, justify="center")
#         console.print()
        
#         # Show user stats
#         if data["roadmaps"]:
#             stats_panel = create_stats_display(data)
#             console.print(stats_panel)
#             console.print()
        
#         # Create and display menu
#         menu_panels = create_menu_panel()
#         columns = Columns(menu_panels, equal=True, expand=True)
#         console.print(columns)
#         console.print()
        
#         # Show motivational tip
#         tip_panel = show_motivational_tip()
#         console.print(tip_panel)
#         console.print()
        
#         # Get user input with style
#         choice_prompt = Text()
#         choice_prompt.append("🎮 Select your choice", style="bold bright_white")
#         choice_prompt.append(" (1-13): ", style="dim")
        
#         console.print(choice_prompt, end="")
#         choice = input().strip()
        
#         if choice.isdigit():
#             idx = int(choice)
            
#             # Add loading animation for better UX
#             if idx in range(1, 14):
#                 console.print(f"\n[dim]Loading option {idx}...[/dim]")
#                 time.sleep(0.5)
            
#             match idx:
#                 case 1:
#                     console.clear()
#                     view_roadmaps(data)
#                     console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
#                     input()
#                 case 2:
#                     console.clear()
#                     create_roadmap(data)
#                     console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
#                     input()
#                 case 3:
#                     console.clear()
#                     add_step(data)
#                     console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
#                     input()
#                 case 4:
#                     console.clear()
#                     mark_step_complete(data)
#                     console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
#                     input()
#                 case 5:
#                     console.clear()
#                     delete(data)
#                     console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
#                     input()
#                 case 6:
#                     console.clear()
#                     view_progress(data)
#                     console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
#                     input()
#                 case 7:
#                     console.clear()
#                     Sort_Roadmaps(data)
#                     console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
#                     input()
#                 case 8:
#                     console.clear()
#                     manage_categories(data)
#                 case 9:
#                     console.clear()
#                     Categories(data)
#                     console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
#                     input()
#                 case 10:
#                     Progress_Visualization(data)
#                     console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
#                     input()
#                 case 11:
#                     console.clear()
#                     edit(data)
#                     console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
#                     input()
#                 case 12:
#                     console.clear()
#                     import_export(data)
#                     console.print(f"\n[dim]Press Enter to return to main menu...[/dim]", end="")
#                     input()
#                 case 13:
#                     # Stylish exit sequence
#                     console.clear()
#                     goodbye_panel = Panel.fit(
#                         "[bold bright_green]🎉 Thank you for using Learning Roadmap Builder! 🎉[/bold bright_green]\n"
#                         "[dim]Keep learning and growing! 🚀[/dim]",
#                         border_style="bright_green",
#                         box=box.DOUBLE
#                     )
#                     console.print(goodbye_panel, justify="center")
#                     console.print("\n[dim]Saving your progress...[/dim]")
#                     time.sleep(1)
#                     console.print("[green]✅ Progress saved successfully![/green]")
#                     time.sleep(0.5)
#                     console.print("[bright_blue]👋 See you next time![/bright_blue]")
#                     break
#                 case _: 
#                     console.print(f"\n[bold red]❌ Invalid choice![/bold red] Please select a number between [bold]1[/bold] and [bold]13[/bold].")
#                     time.sleep(2)
#         else:
#             console.print(f"\n[bold red]❌ Invalid input![/bold red] Please enter a [bold]number[/bold].")
#             time.sleep(2)

# if __name__ == "__main__":
#     main()
#!/usr/bin/env python3
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich import box

# Import all modules
from data_manager import load_data
from ui_components import (
    show_welcome_animation, create_menu_panel, create_stats_display, 
    show_motivational_tip
)

from roadmap_operations import (
    create_roadmap, add_step, mark_step_complete, edit_roadmap, 
    delete_roadmap_or_step, sort_roadmaps
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
        
        # Create and display menu
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
        
        # Show motivational tip
        tip_panel = show_motivational_tip()
        console.print(tip_panel)
        console.print()
        
        # Get user input with style
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


    
