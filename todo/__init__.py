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

class TodoListManager:  
    # Constructor, optional filename parameter with default value 'todolist.json'
    def __init__(self, filename='todolist.json'):
        self.todo_lists = {}
        self.filename = filename
        if os.path.exists(self.filename): 
            self.load_from_file()
        atexit.register(self.save_to_file)  # Automatically call the save_to_file method before exiting

    def create_todo_list(self, name):
        if name in self.todo_lists:
            raise ValueError(f"TodoList named {name} already exists.")
        self.todo_lists[name] = []

    def delete_todo_list(self, name):
        if name not in self.todo_lists:
            raise ValueError(f"No TodoList named {name} found.")
        del self.todo_lists[name]

    def show_all_todo_list(self):
        return self.todo_lists

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

    # Sort the list first, then show it
    def show_all_items_in_todo_list(self, name):
        if name not in self.todo_lists:
            raise ValueError(f"No TodoList named {name} found.")
        formatted_items = []
        for item_data in sorted(
                self.todo_lists[name],
                key=lambda x: (x['priority'], x['due_date'] if x['due_date'] is not None else datetime.max.date()) # priority > due_date, and we give date a default max value to represent no due date (very low priority)
            ):
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

    def remove_item_from_todo_list(self, name, index):
        if name not in self.todo_lists:
            raise ValueError(f"No TodoList named {name} found.")
        try:
            del self.todo_lists[name][index]
        except IndexError:
            raise IndexError(f"No item at index {index} in TodoList {name}.")
    
    # Save to json file using the custom encoder
    def save_to_file(self):
        with open(self.filename, 'w') as f:
            json.dump(self.todo_lists, f, cls=CustomEncoder)

    # Restore the list from the json file
    def load_from_file(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        # Custom decoding for the loaded data
        for todo_list_name, tasks in data.items():
            for task in tasks:
                if 'due_date' in task and task['due_date'] is not None:
                    task['due_date'] = datetime.strptime(task['due_date'], '%Y-%m-%d').date() # Restore due_date field
                if 'priority' in task and task['priority'] == "Infinity":
                    task['priority'] = float('inf') # Restore priority field
            if todo_list_name not in self.todo_lists:
                self.todo_lists[todo_list_name] = {}
            else:
                self.todo_lists[todo_list_name].clear()
            for task in tasks:
                self.add_item_to_todo_list(todo_list_name, task['name'], priority=task['priority'], due_date=task['due_date'])
