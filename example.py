from todo import TodoListManager
import os

file_path = "todo.json"

if os.path.exists(file_path):
    os.remove(file_path)

manager = TodoListManager(file_path)
manager.create_todo_list('Groceries')
manager.add_item_to_todo_list('Groceries', 'Apple', priority=1, due_date="2023-11-10")

del manager  

new_manager = TodoListManager(file_path)

assert 'Groceries' not in new_manager.show_all_todo_list(), "New manager should not have any todo lists before loading"

try:
    new_manager.load_from_file()
except ValueError as e:
    print(f"A ValueError occurred: {e}")

assert 'Groceries' in new_manager.show_all_todo_list(), "Todo list 'Groceries' should be present after loading"
assert 'Apple' in [item['item'] for item in new_manager.todo_lists['Groceries']], "Item 'Apple' should be present in 'Groceries' todo list"

print("All tests passed!")