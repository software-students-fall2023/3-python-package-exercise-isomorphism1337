from .todo import TodoListManager

def main():
    # Instantiate the TodoListManager, we don't restore from the last call
    manager = TodoListManager(enable_auto_restore = False)

    # Demonstrate creating a new todo list
    print("Creating a new todo list named 'Groceries'...")
    manager.create_todo_list('Groceries')
    manager.create_todo_list('Groceries')

    # Demonstrate adding items to the todo list
    print("Adding items to 'Groceries' list...")
    manager.add_item_to_todo_list('Groceries', 'Apple', priority=1, due_date="2023-11-10")
    manager.add_item_to_todo_list('Groceries', 'Banana', priority=2)
    manager.add_item_to_todo_list('Groceries', 'Carrot', due_date="2023-12-01")

    # Demonstrate showing all todo lists
    print("\nAll Todo Lists:")
    manager.print_all_todo_lists()

    # Demonstrate showing items in a specific todo list
    print("\nItems in 'Groceries' list:")
    items = manager.show_all_items_in_todo_list('Groceries')
    for item in items:
        print(item)

    # Demonstrate deleting an item from the todo list
    print("\nRemoving 'Banana' from 'Groceries' list...")
    manager.remove_item_from_todo_list('Groceries', 1)

    # Show remaining items in the todo list
    print("\nItems in 'Groceries' list after removal:")
    items = manager.show_all_items_in_todo_list('Groceries')
    for item in items:
        print(item)

    # Demonstrate changing the name of a todo list
    print("\nChanging 'Groceries' list name to 'Supermarket'...")
    manager.change_todo_list_name('Groceries', 'Supermarket')

    # Demonstrate showing all todo lists after renaming
    print("\nAll Todo Lists after renaming:")
    print(manager.show_all_todo_list())

if __name__ == "__main__":
    main()