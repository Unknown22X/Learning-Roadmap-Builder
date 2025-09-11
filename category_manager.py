from data_manager import save_data

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