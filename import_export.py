import json
from data_manager import save_data

def import_export_roadmaps(data):
    print(f"\n[Import/Export Roadmaps]")
    print("1. Export roadmap")
    print("2. Import roadmap")
    choice = input("Select option: ").strip()
    if choice.isdigit():
        choice = int(choice)
        if choice not in [1, 2]:
            print("Number must be 1 or 2.")
            return
    else:
        print("Invalid input. Please enter a number.")
        return
        
    if choice == 1:
        if not data["roadmaps"]:
            print("No roadmaps to export")
            return
        for i, roadmap in enumerate(data["roadmaps"], start=1):
            print(f"{i}. {roadmap['title']}")
        while True: 
            idx = input("Enter roadmap number: ").strip()
            if idx.isdigit() and 1 <= int(idx) <= len(data['roadmaps']):
                idx = int(idx) - 1
                break
            print("Invalid input")
        filename = input(f"Enter export filename (e.g, roadmap.json): ").strip()
        try: 
            with open(filename, "w") as f:
                json.dump(data["roadmaps"][idx], f, indent=4)
                print(f"Roadmap exported to '{filename}'.")
        except IOError as e:
            print(f"Error writing to file: {e}")
            
    elif choice == 2:
        filename = input("Enter import filename: ").strip()
        try:
            with open(filename, "r") as f:
                roadmap = json.load(f)
            data["roadmaps"].append(roadmap)
            save_data(data)
            print(f"Roadmap '{roadmap['title']}' imported.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Invalid file or JSON format.")