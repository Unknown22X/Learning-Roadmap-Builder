import json
import rich
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
            data =  {"roadmaps": []} 
    return data



def save_data(data) :
          with open ("data.json" , "w") as f :
                 json.dump(data, f, indent=4)

def create_roadmap(data) :

        print("[Create Roadmap]")

        title = input("Enter The title for the road maps : ").strip()
        if title:
                data["roadmaps"].append({"title": title, "steps": []})
                save_data(data)
                print(f"Roadmap '{title}' created.")


def view_roadmaps(data):

    print("\n[View Roadmaps]")
    if not data["roadmaps"]:
        print("No roadmaps found.\n")
        return

    for roadmap in data["roadmaps"]:
        print(f"\n=== Roadmap: {roadmap['title']} ===\n")
        steps = roadmap.get("steps", [])
        if steps:
            for i, step in enumerate(steps, start=1):
                
                status = "done" if step.get("done", False) else "not done"
                print(f"  {i}. {step['title']} | {status}")
        else:
            print("  (No steps yet)")
        print("=" * 30)
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
        for i in range (len(steps)):
           step = steps[i] 
           print(f"{i+1}. {step['title']}")
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


def view_progress() :
     pass
def Sort_Roadmaps() :
        print("\n[Sort Roadmaps]")
        pass
def Categories() :
     pass

def Progress_Visualization() :
     pass
def import_export()  :
     pass

def edit(data):
#      Edit Roadmap/Step
        # print("\n[Edit Roadmap/Step]")
        # roadmaps = data["roadmaps"]
        # if not roadmaps:
        #         print("No roadmaps available.")
        #         return

        # print("\nSelect a roadmap to edit:")
        # for i, roadmap in enumerate(roadmaps, start=1):
        #         print(f"{i}. {roadmap['title']}")
        # while True:
        #         roadmap_num = input("Enter roadmap number (or 'q' to quit): ").strip()
        #         if roadmap_num.lower() == "q":
        #                 return
        #         if roadmap_num.isdigit() and 1 <= int(roadmap_num) <= len(roadmaps):
        #                 roadmap_idx = int(roadmap_num) - 1
        #                 break
        #         print("Invalid input. Please try again.")

        # print("\nEdit options:")
        # print("1. Edit roadmap title")
        # print("2. Edit step title")
        # while True:
        #         option = input("Select option: ").strip()
        #         if option in ("1", "2"):
        #                 break
        #         print("Invalid input. Please enter 1 or 2.")

        # if option == "1":
        #         new_title = input("Enter new roadmap title: ").strip()
        #         if new_title:
        #                 old_title = roadmaps[roadmap_idx]["title"]
        #                 roadmaps[roadmap_idx]["title"] = new_title
        #                 save_data(data)
        #                 print(f"Roadmap title changed from '{old_title}' to '{new_title}'.")
        #         else:
        #                 print("Title cannot be empty.")
        # else:
        #         steps = roadmaps[roadmap_idx]["steps"]
        #         if not steps:
        #                 print("This roadmap has no steps yet.")
        #                 return
        #         print("\nSelect a step to edit:")
        #         for i, step in enumerate(steps, start=1):
        #                 print(f"{i}. {step['title']}")
        #         while True:
        #                 step_num = input("Enter step number: ").strip()
        #                 if step_num.isdigit() and 1 <= int(step_num) <= len(steps):
        #                         step_idx = int(step_num) - 1
        #                         break
        #                 print("Invalid input. Please try again.")
        #         new_step_title = input("Enter new step title: ").strip()
        #         if new_step_title:
        #                 old_step_title = steps[step_idx]["title"]
        #                 steps[step_idx]["title"] = new_step_title
        #                 save_data(data)
        #                 print(f"Step title changed from '{old_step_title}' to '{new_step_title}'.")
        #         else:
        #                 print("Step title cannot be empty.")
        pass
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
[6] Exit
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
                    print("Exiting .......")
                    break
                case _:
                    print("invalid choice")
         else:
          print("Invalid input. Please enter a number from the menu.")
if __name__ == "__main__":
    main()
