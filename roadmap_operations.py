from data_manager import save_data

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
    if not title or title.isspace():
        print("Title cannot be empty or just spaces.")
        return
    if title:
        data["roadmaps"].append({
            "title": title, 
            "category": category,
            "steps": []
        })
        save_data(data)
        print(f"Roadmap '{title}' created in category '{category}'.")

def add_step(data):
    # select which task 
    print("\n[3] add step")

    roadmaps = data["roadmaps"]
    if not roadmaps:
        print("No roadmaps available.")
        return
    print("\nSelect a roadmap (or 'q' to quit):")
    for i, roadmap in enumerate(roadmaps, start=1):
        print(f"{i}. {roadmap['title']}")
    while True: 
        task = input("Enter roadmap number: ").strip()
        if task.lower() == "q":
            return
        if task.isdigit() and 1 <= int(task) <= len(roadmaps):
            idx = int(task) - 1
            break
        print("Invalid input. Please try again.")
    # add a step to this task 

    step_title = input("Enter step title: ").strip()
    if not step_title:
        print("Step title cannot be empty.")
        return
    if step_title:
        roadmaps[idx]["steps"].append({"title": step_title, "done": False})
        save_data(data)
        print(f"Step '{step_title}' added to '{roadmaps[idx]['title']}'.")

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

    for i, roadmap in enumerate(roadmaps, start=1):
        print(f"{i}. {roadmap['title']}")

    while True:
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

    elif oper == 2:
        steps = roadmaps[roadmap_idx]["steps"]
        if not steps:
            print("This roadmap has no steps yet.")
            return
        print("\n=== Select a step to delete by typing its number ===")
        for i in range(len(steps)):
            print(f"{i+1}. {steps[i]['title']}")
        while True: 
            step_num = input("Enter step num : ")
            if step_num.isdigit(): 
                idxS = int(step_num)
                if 1 <= idxS <= len(steps):
                    idxS = idxS - 1  # Convert to 0-based for internal use
                    break
            print("Invalid input. Please enter a valid number.")
        confirm = input(f"Are you sure you want to delete '{steps[idxS]['title']}'? (y/n): ").strip().lower()
        if confirm != "y":
            print("Deletion canceled.")
            return
        deleted = steps.pop(idxS)
        save_data(data)
        print(f"Step '{deleted['title']}' deleted from roadmap '{roadmaps[roadmap_idx]['title']}'.")