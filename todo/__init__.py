import atexit
import json
import os
from datetime import date, datetime

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
    def __init__(self, filename='todolist.json', enable_auto_save = True):
        self.todo_lists = {}
        self.filename = os.path.abspath(filename)
        if os.path.exists(self.filename): 
            self.load_from_file()
        if enable_auto_save:
            atexit.register(self.save_to_file)  # Automatically save the created lists to the file named filename

    # Create a new todo list
    def create_todo_list(self, name):
        if name in self.todo_lists:
            raise ValueError(f"TodoList named {name} already exists.")
        self.todo_lists[name] = []

    # Delete a certain todo list
    def delete_todo_list(self, name):
        if name not in self.todo_lists:
            raise ValueError(f"No TodoList named {name} found.")
        del self.todo_lists[name]

    # Show all todo lists
    def show_all_todo_list(self):
        return self.todo_lists

    # Change todo list name
    def change_todo_list_name(self, old_name, new_name):
        if old_name not in self.todo_lists:
            raise ValueError(f"No TodoList named {old_name} found.")
        if new_name in self.todo_lists:
            raise ValueError(f"TodoList named {new_name} already exists.")
        self.todo_lists[new_name] = self.todo_lists.pop(old_name)

    # Maintain two optional fields used for sorting, priority field has higher priority than due_date field
    def add_item_to_todo_list(self, name, item, priority=None, due_date=None):
        if name not in self.todo_lists:
            raise ValueError(f"No TodoList named {name} found.")
        item_data = {'item': item, 'priority': priority if priority is not None else float('inf')}
        if due_date:
            try:
                item_data['due_date'] = datetime.strptime(due_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format.")
        else:
            item_data['due_date'] = None
        self.todo_lists[name].append(item_data)
        # Sort the list after insertion
        self.todo_lists[name].sort(
            key=lambda x: (x['priority'], x['due_date'] if x['due_date'] is not None else datetime.max.date())
        )

    # Return list in a user-friendly format
    def show_all_items_in_todo_list(self, name):
        if name not in self.todo_lists:
            raise ValueError(f"No TodoList named {name} found.")
        formatted_items = []
        for item_data in self.todo_lists[name]:
            item_string = f"Item: {item_data['item']}"
            if item_data['priority'] == float('inf'):
                item_string += ", Priority: No priority specified" # format the returned list to be more user-friendly
            else:
                item_string += f", Priority: {item_data['priority']}"  
            if item_data['due_date'] is None:
                item_string += ", Due date: No due date" # format the returned list to be more user-friendly
            else:
                item_string += f", Due date: {item_data['due_date'].strftime('%Y-%m-%d')}"
            formatted_items.append(item_string)
        return formatted_items

    # Remove an item from the specified todo list
    def remove_item_from_todo_list(self, name, index):
        if name not in self.todo_lists:
            raise ValueError(f"No TodoList named {name} found.")
        try:
            del self.todo_lists[name][index]
        except IndexError:
            raise IndexError(f"No item at index {index} in TodoList {name}.")
        # Sort the list after deletion
        self.todo_lists[name].sort(
            key=lambda x: (x['priority'], x['due_date'] if x['due_date'] is not None else datetime.max.date())
        )
    
    # Save to json file using the custom encoder
    def save_to_file(self):
        with open(self.filename, 'w') as f:
            json.dump(self.todo_lists, f, cls = CustomEncoder)

    # Restore the list from the json file
    def load_from_file(self):
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