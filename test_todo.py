# We still need more test functions for the constructor, show_all_todo_list, show_all_items_in_todo_list, save_to_file, load_from_file
# All others are added :)

from todo import TodoListManager
import pytest

# Fixture for manager setup
@pytest.fixture
def manager(tmpdir):
    filename = tmpdir.join("todo.json")  
    manager = TodoListManager(str(filename))
    return manager

#--------------------------------------------------------------------------------------------
# Three test functions for create_todo_list function
def test_create_todo_list(manager):
    manager.create_todo_list("Groceries")
    assert "Groceries" in manager.todo_lists

def test_create_existing_todo_list(manager):
    manager.create_todo_list("Groceries")
    with pytest.raises(ValueError, match = r"TodoList named Groceries already exists."):
        manager.create_todo_list("Groceries")
        
def test_create_todo_list_data_integrity(manager):
    manager.create_todo_list('Hobbies')
    assert isinstance(manager.todo_lists['Hobbies'], list)
    assert len(manager.todo_lists['Hobbies']) == 0
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Three test functions for delete_todo_list function
def test_delete_todo_list(manager):
    manager.create_todo_list("Groceries")
    manager.delete_todo_list("Groceries")
    assert "Groceries" not in manager.todo_lists

def test_delete_nonexistent_todo_list(manager):
    with pytest.raises(ValueError, match = r"No TodoList named Groceries found."):
        manager.delete_todo_list("Groceries")
        
def test_delete_todo_list_does_not_affect_others(manager):
    manager.create_todo_list('Groceries')
    manager.create_todo_list('Chores')
    manager.delete_todo_list('Groceries')
    assert 'Groceries' not in manager.todo_lists
    assert 'Chores' in manager.todo_lists
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Three test functions for change_todo_list_name function
def test_change_todo_list_name(manager):
    manager.create_todo_list("Groceries")
    manager.change_todo_list_name("Groceries", "Supermarket")
    assert "Supermarket" in manager.todo_lists
    assert "Groceries" not in manager.todo_lists

def test_change_todo_list_name_to_existing_name(manager):
    manager.create_todo_list("Groceries")
    manager.create_todo_list("Supermarket")
    with pytest.raises(ValueError, match = r"TodoList named Supermarket already exists."):
        manager.change_todo_list_name("Groceries", "Supermarket")
        
def test_change_nonexistent_todo_list_name(manager):
    manager.create_todo_list("Groceries")
    with pytest.raises(ValueError, match = r"No TodoList named Supermarket found."):
        manager.change_todo_list_name("Supermarket", "Groceries")
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Five test functions for add_item_to_todo_list function
def test_add_item_to_todo_list(manager):
    manager.create_todo_list("Groceries")
    manager.add_item_to_todo_list("Groceries", "Milk")
    manager.add_item_to_todo_list("Groceries", "Eggs")
    manager.add_item_to_todo_list("Groceries", "Bread")
    items = manager.show_all_items_in_todo_list("Groceries")
    assert items == [
        "Item: Milk, Priority: No priority specified, Due date: No due date",
        "Item: Eggs, Priority: No priority specified, Due date: No due date",
        "Item: Bread, Priority: No priority specified, Due date: No due date"
    ]

def test_add_item_to_todo_list_priority_only(manager):
    manager.create_todo_list("Groceries")
    manager.add_item_to_todo_list("Groceries", "Milk", 2)
    manager.add_item_to_todo_list("Groceries", "Eggs", 1)
    manager.add_item_to_todo_list("Groceries", "Bread")
    manager.add_item_to_todo_list("Groceries", "Butter", 3)
    items = manager.show_all_items_in_todo_list("Groceries")
    expected_items = [
        "Item: Eggs, Priority: 1, Due date: No due date",
        "Item: Milk, Priority: 2, Due date: No due date",
        "Item: Butter, Priority: 3, Due date: No due date",
        "Item: Bread, Priority: No priority specified, Due date: No due date"
    ]
    assert items == expected_items

def test_add_item_to_todo_list_due_date_and_priority(manager):
    manager.create_todo_list("Homework")
    manager.add_item_to_todo_list("Homework", "Midterm Review", 1, "2023-11-10")
    manager.add_item_to_todo_list("Homework", "Essay", 2, "2023-11-09")
    items = manager.show_all_items_in_todo_list("Homework")
    assert items == [
        "Item: Midterm Review, Priority: 1, Due date: 2023-11-10",
        "Item: Essay, Priority: 2, Due date: 2023-11-09"
    ]

def test_add_item_to_todo_list_due_date_only(manager):
    manager.create_todo_list("Reading")
    manager.add_item_to_todo_list("Reading", "Chapter 1", due_date="2023-11-15")
    manager.add_item_to_todo_list("Reading", "Chapter 2", due_date="2023-11-22")
    items = manager.show_all_items_in_todo_list("Reading")
    assert items == [
        "Item: Chapter 1, Priority: No priority specified, Due date: 2023-11-15",
        "Item: Chapter 2, Priority: No priority specified, Due date: 2023-11-22"
    ]

def test_add_item_to_nonexistent_todo_list(manager):
    manager.create_todo_list("Groceries")
    with pytest.raises(ValueError, match = r"No TodoList named Supermarket found."):
        manager.add_item_to_todo_list("Supermarket", "Bread")
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Three test functions for remove_item_from_todo_list function
def test_remove_item_from_todo_list(manager):
    manager.create_todo_list("Groceries")
    manager.add_item_to_todo_list("Groceries", "Milk")
    manager.remove_item_from_todo_list("Groceries", 0)
    assert "Milk" not in manager.show_all_items_in_todo_list("Groceries")

def test_remove_item_from_todo_list_invalid_index(manager):
    manager.create_todo_list("Groceries")
    with pytest.raises(IndexError, match=r"No item at index 0 in TodoList Groceries."):
        manager.remove_item_from_todo_list("Groceries", 0)
        
def test_remove_item_from_nonexistent_list(manager):
    manager.create_todo_list("Groceries")
    with pytest.raises(ValueError, match = r"No TodoList named Supermarket found."):
        manager.remove_item_from_todo_list("Supermarket", 0)
#--------------------------------------------------------------------------------------------

# Test if the lists are saved correctly
def test_save_to_file(manager, tmpdir):
    manager.create_todo_list("Groceries")
    manager.save_to_file()  
    file_path = tmpdir.join("todo.json")
    assert file_path.read() == '{"Groceries": []}'

# Test if the lists are recovered correctly
def test_load_from_file(manager, tmpdir):
    file_path = tmpdir.join("todo.json")
    file_path.write('{"Groceries": []}')
    manager.load_from_file()  
    assert "Groceries" in manager.todo_lists
