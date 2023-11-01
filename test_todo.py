from todo import TodoListManager
import pytest

# Fixture for manager setup
@pytest.fixture
def manager():
    return TodoListManager()

def test_create_todo_list(manager):
    manager.create_todo_list("Groceries")
    assert "Groceries" in manager.todo_lists

def test_create_existing_todo_list(manager):
    manager.create_todo_list("Groceries")
    with pytest.raises(ValueError, match=r"TodoList named Groceries already exists."):
        manager.create_todo_list("Groceries")

def test_delete_todo_list(manager):
    manager.create_todo_list("Groceries")
    manager.delete_todo_list("Groceries")
    assert "Groceries" not in manager.todo_lists

def test_delete_nonexistent_todo_list(manager):
    with pytest.raises(ValueError, match=r"No TodoList named Groceries found."):
        manager.delete_todo_list("Groceries")

def test_change_todo_list_name(manager):
    manager.create_todo_list("Groceries")
    manager.change_todo_list_name("Groceries", "Supermarket")
    assert "Supermarket" in manager.todo_lists
    assert "Groceries" not in manager.todo_lists

def test_change_todo_list_name_to_existing_name(manager):
    manager.create_todo_list("Groceries")
    manager.create_todo_list("Supermarket")
    with pytest.raises(ValueError, match=r"TodoList named Supermarket already exists."):
        manager.change_todo_list_name("Groceries", "Supermarket")

def test_add_item_to_todo_list(manager):
    manager.create_todo_list("Groceries")
    manager.add_item_to_todo_list("Groceries", "Milk")
    assert "Milk" in manager.show_all_items_in_todo_list("Groceries")

def test_show_all_items_in_todo_list(manager):
    manager.create_todo_list("Groceries")
    manager.add_item_to_todo_list("Groceries", "Milk")
    assert "Milk" in manager.show_all_items_in_todo_list("Groceries")

def test_remove_item_from_todo_list(manager):
    manager.create_todo_list("Groceries")
    manager.add_item_to_todo_list("Groceries", "Milk")
    manager.remove_item_from_todo_list("Groceries", 0)
    assert "Milk" not in manager.show_all_items_in_todo_list("Groceries")

def test_remove_item_from_todo_list_invalid_index(manager):
    manager.create_todo_list("Groceries")
    with pytest.raises(IndexError, match=r"No item at index 0 in TodoList Groceries."):
        manager.remove_item_from_todo_list("Groceries", 0)
