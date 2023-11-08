from .todo import TodoListManager

# Simple example function to demonstrate how to use todopkg package
def main():
    # Initialize the TodoListManager
    manager = TodoListManager(enable_auto_restore=False)  # Assuming you don't want to load from the Json file right now

    # Create a couple of todo lists
    print("\nCreating two todo lists...\n")
    manager.create_todo_list("Chores")
    manager.create_todo_list("Work")

    # Add items to the todo lists
    print("Add items to the todo lists...\n")
    manager.add_item_to_todo_list("Chores", "Wash dishes", priority=2, due_date='2023-12-01')
    manager.add_item_to_todo_list("Chores", "Take out trash", priority=1, due_date='2023-11-25')
    manager.add_item_to_todo_list("Work", "Finish report", priority=1, due_date='2023-11-30')
    manager.add_item_to_todo_list("Work", "Email client", priority=2)

    # Show all items in a specific todo list
    print("Items in Chores list:")
    print(manager.show_all_items_in_todo_list("Chores"))
    print("\nItems in Work list:")
    print(manager.show_all_items_in_todo_list("Work"))

    # Show all todo list in raw format
    print("\nShow all todo list in raw format:")
    print(manager.show_all_todo_list())

    # Change the name of a todo list
    print("\nChange the name of todo list 'Chores' to 'Household Tasks...'")
    manager.change_todo_list_name("Chores", "Household Tasks")

    # Remove an item from a todo list
    print("\nRemove todo 'Wash dishes' from 'Household Tasks' list")
    manager.remove_item_from_todo_list("Household Tasks", 0)

    # Print the lists in table format
    print("\nAll lists after removal:")
    manager.print_all_todo_lists()

    # Attempt to delete a todo list
    print("Delete todo list 'Work'")
    manager.delete_todo_list("Work")
    print("\nAll lists after deletion:")
    manager.print_all_todo_lists()

    # Demonstrate save to file and load from file
    print("\nSaving lists to file.\n")
    manager.save_to_file()
    print("Clearing all lists from manager.\n")
    manager.todo_lists.clear()
    print("Loading lists from file.")
    manager.load_from_file()
    print("\nAll lists after loading from file:")
    manager.print_all_todo_lists()

if __name__ == "__main__":
    main()