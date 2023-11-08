import atexit
import json
import os
from datetime import date, datetime
from tabulate import tabulate

# Class to encode the due date and priority when saving the lists to the json file
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, float) and obj == float('inf'):
            return "Infinity"
        return json.JSONEncoder.default(self, obj)

# Main todo list class
class TodoListManager:  
    
    # Constructor, optional filename parameter with default value 'todolist.json'
    def __init__(self, filename='todolist.json', enable_auto_restore=True):
        self.todo_lists = {}
        self.filename = filename
        # Attempt to load from file, proceed regardless of errors
        if os.path.exists(self.filename) and enable_auto_restore:
            try:
                self.load_from_file()
            except Exception as e:  # Catch any exception that load_from_file could raise
                print(f"Warning: An error occurred while loading the file. Proceeding without loading. Error: {e}")
        # Register save_to_file to execute upon program exit
        atexit.register(self.save_to_file)

    # Create a new todo list
    def create_todo_list(self, name):
        try:
            if name in self.todo_lists:
                raise ValueError(f"TodoList named {name} already exists.")
            self.todo_lists[name] = []
            self.save_to_file()
        except ValueError as e:
            print(f"Error: {e}")
            return False
        return True

    # Delete a certain todo list
    def delete_todo_list(self, name):
        if name not in self.todo_lists:
            print(f"No TodoList named '{name}' found.")
            return False
        del self.todo_lists[name]
        print(f"TodoList named '{name}' deleted")
        self.save_to_file()
        return True

    # Show all todo lists
    def show_all_todo_list(self):
        return self.todo_lists

    # Change todo list name
    def change_todo_list_name(self, old_name, new_name):
        if old_name not in self.todo_lists:
            print(f"No TodoList named '{old_name}' found.")
            return f"No TodoList named '{old_name}' found."
        if new_name in self.todo_lists:
            print(f"TodoList named '{new_name}' already exists.")
            return f"TodoList named '{new_name}' already exists."
        self.todo_lists[new_name] = self.todo_lists.pop(old_name)
        print(f"Successfully changed TodoList '{old_name}' to '{new_name}'")
        self.save_to_file()
        return True

    # Maintain two optional fields used for sorting, priority field has higher priority than due_date field
    def add_item_to_todo_list(self, name, item, priority=None, due_date=None):
        if name not in self.todo_lists:
            print(f"No TodoList named {name} found.")
            return f"No TodoList named {name} found."
        for existing_item in self.todo_lists[name]:
            if existing_item['item'] == item:
                print(f"Item {item} already exists in the TodoList {name}.")
                return "Item already exists in the TodoList."
        if priority is not None and priority != float('inf'):
            if not isinstance(priority, int) or priority < 0:
                print("Priority must be a non-negative integer.")
                return "Priority must be a non-negative integer."
        item_data = {'item': item, 'priority': priority if priority is not None else float('inf')}
        if due_date:
            try:
                item_data['due_date'] = datetime.strptime(due_date, "%Y-%m-%d").date()
            except ValueError:
                print("Due date must be in YYYY-MM-DD format.")
                return "Due date must be in YYYY-MM-DD format."
        else:
            item_data['due_date'] = None
        self.todo_lists[name].append(item_data)
        # Sort the list after insertion
        self.todo_lists[name].sort(
            key=lambda x: (x['priority'], x['due_date'] if x['due_date'] is not None else datetime.max.date())
        )
        self.save_to_file()
        return "Item added successfully."

    # Return list in a user-friendly format
    def show_all_items_in_todo_list(self, name):
        if name not in self.todo_lists:
            print(f"No TodoList named {name} found.")
            return f"No TodoList named {name} found."  # Returning a message instead of raising an error
        formatted_items = []
        for item_data in self.todo_lists[name]:
            item_string = f"Item: {item_data['item']}"
            if item_data['priority'] == float('inf'):
                item_string += ", Priority: No priority specified"  # format the returned list to be more user-friendly
            else:
                item_string += f", Priority: {item_data['priority']}"  
            if item_data['due_date'] is None:
                item_string += ", Due date: No due date"  # format the returned list to be more user-friendly
            else:
                item_string += f", Due date: {item_data['due_date'].strftime('%Y-%m-%d')}"
            formatted_items.append(item_string)
        return formatted_items
    
    # Print all todo lists (or a single todo list) in a table format
    def print_all_todo_lists(self, list_name = None):
        lists_to_print = self.show_all_todo_list().items()
        if list_name:  # If a specific list name is provided
            if list_name in self.todo_lists:
                lists_to_print = [(list_name, self.todo_lists[list_name])]
            else:
                print(f"No TodoList named '{list_name}' found.")
                return False
        for name, items in lists_to_print:
            title = f"Todo List: {name}"
            separator = "-" * (11 + len(title))
            print(separator)
            print(title)
            print(separator)
            if not items:
                print("This TodoList is empty.")
                continue
            table = []
            headers = ["Item", "Priority", "Due Date"]
            for item in items:
                priority = 'N/A' if item['priority'] == float('inf') else item['priority']
                due_date = item['due_date'].strftime('%Y-%m-%d') if item['due_date'] else 'No due date'
                table.append([item['item'], priority, due_date])
            print(tabulate(table, headers, tablefmt="grid"))
            print()
        return True
            
    # Remove an item from the specified todo list
    def remove_item_from_todo_list(self, name, index):
        if name not in self.todo_lists:
            print(f"No TodoList named {name} found.")
            return f"No TodoList named {name} found."
        if not isinstance(index, int):
            print(f"Invalid index: {index}. Index must be an integer.")
            return f"Invalid index: {index}. Index must be an integer."
        if not isinstance(index, int) or index < 0 or index >= len(self.todo_lists[name]):
            print(f"Index {index} is out of range for TodoList {name}.")
            return f"Index {index} is out of range for TodoList {name}."
        del self.todo_lists[name][index]
        # Sort the list after deletion
        self.todo_lists[name].sort(
            key=lambda x: (x['priority'], x['due_date'] if x['due_date'] is not None else datetime.max.date())
        )
        self.save_to_file()
        print(f"Item at index {index} removed from TodoList {name}.")
        return f"Item at index {index} removed from TodoList {name}."
    
    # Save to json file using the custom encoder
    def save_to_file(self):
        with open(self.filename, 'w') as f:
            json.dump(self.todo_lists, f, cls = CustomEncoder)

    # Restore the list from the json file
    def load_from_file(self):
        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"The file {self.filename} does not exist.")
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("The file could not be decoded as JSON.")
        # Ensure that the data is a dictionary
        if not isinstance(data, dict):
            raise ValueError("The file does not contain a valid todo list format.")
        for todo_list_name, tasks in data.items():
            # Validate that tasks is a list of dictionaries
            if not isinstance(tasks, list) or not all(isinstance(task, dict) for task in tasks):
                raise ValueError(f"Tasks for {todo_list_name} are not in a valid format.")
            # if todo_list_name not in self.todo_lists:
            self.create_todo_list(todo_list_name)
            for task in tasks:
                item_name = task.get('item')
                priority = task.get('priority')
                due_date = task.get('due_date')  # This should be a string in the format 'YYYY-MM-DD'
                if priority == "Infinity":
                    priority = float('inf')
                elif not isinstance(priority, (int, float)):
                    raise ValueError(f"Invalid priority for {item_name} in {todo_list_name}.")
                # Add the task to the todo list
                self.add_item_to_todo_list(todo_list_name, item_name, priority=priority, due_date=due_date)
