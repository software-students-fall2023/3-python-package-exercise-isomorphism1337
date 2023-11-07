from src.todopkg.todo import TodoListManager
from src.todopkg.todo import CustomEncoder
from datetime import date
import pytest
import os
import json

# Fixture for manager setup
@pytest.fixture
def manager(tmpdir):
    filename = tmpdir.join("todo.json")  
    manager = TodoListManager(str(filename))
    return manager

#--------------------------------------------------------------------------------------------
# Three test functions for create_todo_list function
def test_create_todo_list(manager):
    result = manager.create_todo_list("Groceries")
    assert "Groceries" in manager.todo_lists
    assert result is True  

def test_create_existing_todo_list(manager):
    manager.create_todo_list("Groceries")
    result = manager.create_todo_list("Groceries")
    assert result is False  
    assert "Groceries" in manager.todo_lists  

def test_create_todo_list_data_integrity(manager):
    result = manager.create_todo_list('Hobbies')
    assert isinstance(manager.todo_lists['Hobbies'], list)
    assert len(manager.todo_lists['Hobbies']) == 0
    assert result is True  
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Three test functions for delete_todo_list function
def test_delete_todo_list(manager):
    manager.create_todo_list("Groceries")
    deleted = manager.delete_todo_list("Groceries")
    assert deleted is True
    assert "Groceries" not in manager.todo_lists

def test_delete_nonexistent_todo_list(manager):
    deleted = manager.delete_todo_list("Groceries")
    assert deleted is False

def test_delete_todo_list_does_not_affect_others(manager):
    manager.create_todo_list('Groceries')
    manager.create_todo_list('Chores')
    manager.delete_todo_list('Groceries')
    assert 'Groceries' not in manager.todo_lists
    assert 'Chores' in manager.todo_lists
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Four test functions for show_all_todo_list function
def test_show_all_todo_list_empty(manager):
    assert manager.show_all_todo_list() == {}

def test_show_all_todo_list_single(manager):
    manager.create_todo_list('Groceries')
    all_lists = manager.show_all_todo_list()
    assert 'Groceries' in all_lists

def test_show_all_todo_list_multiple(manager):
    lists_to_create = ['Groceries', 'Chores', 'Work']
    for list_name in lists_to_create:
        manager.create_todo_list(list_name)
    all_lists = manager.show_all_todo_list()
    assert len(all_lists) == len(lists_to_create)
    for list_name in lists_to_create:
        assert list_name in all_lists

def test_show_all_todo_list_consistency(manager):
    manager.create_todo_list('Groceries')
    manager.create_todo_list('Chores')
    manager.delete_todo_list('Groceries')
    manager.create_todo_list('Work')
    all_lists = manager.show_all_todo_list()
    assert 'Chores' in all_lists
    assert 'Work' in all_lists
    assert 'Groceries' not in all_lists
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Three test functions for change_todo_list_name function
def test_change_todo_list_name(manager):
    manager.create_todo_list("Groceries")
    change_status = manager.change_todo_list_name("Groceries", "Supermarket")
    assert change_status is True
    assert "Supermarket" in manager.todo_lists
    assert "Groceries" not in manager.todo_lists

def test_change_todo_list_name_to_existing_name(manager):
    manager.create_todo_list("Groceries")
    manager.create_todo_list("Supermarket")
    change_status = manager.change_todo_list_name("Groceries", "Supermarket")
    assert change_status is False

def test_change_nonexistent_todo_list_name(manager):
    change_status = manager.change_todo_list_name("Supermarket", "Groceries")
    assert change_status is False
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Seven test functions for add_item_to_todo_list function.
def test_add_item_to_todo_list(manager):
    manager.create_todo_list("Groceries")
    assert manager.add_item_to_todo_list("Groceries", "Milk") == "Item added successfully."
    assert manager.add_item_to_todo_list("Groceries", "Eggs") == "Item added successfully."
    assert manager.add_item_to_todo_list("Groceries", "Bread") == "Item added successfully."
    items = manager.show_all_items_in_todo_list("Groceries")
    assert len(items) == 3

def test_add_item_to_todo_list_priority_only(manager):
    manager.create_todo_list("Groceries")
    assert manager.add_item_to_todo_list("Groceries", "Milk", 2) == "Item added successfully."
    assert manager.add_item_to_todo_list("Groceries", "Eggs", 1) == "Item added successfully."
    assert manager.add_item_to_todo_list("Groceries", "Bread") == "Item added successfully."
    assert manager.add_item_to_todo_list("Groceries", "Butter", 3) == "Item added successfully."
    items = manager.show_all_items_in_todo_list("Groceries")
    assert items == [
        "Item: Eggs, Priority: 1, Due date: No due date",
        "Item: Milk, Priority: 2, Due date: No due date",
        "Item: Butter, Priority: 3, Due date: No due date",
        "Item: Bread, Priority: No priority specified, Due date: No due date"
    ]

def test_add_item_to_todo_list_due_date_and_priority(manager):
    manager.create_todo_list("Homework")
    assert manager.add_item_to_todo_list("Homework", "Midterm Review", 1, "2023-11-10") == "Item added successfully."
    assert manager.add_item_to_todo_list("Homework", "Essay", 2, "2023-11-09") == "Item added successfully."
    items = manager.show_all_items_in_todo_list("Homework")
    assert items == [
        "Item: Midterm Review, Priority: 1, Due date: 2023-11-10",
        "Item: Essay, Priority: 2, Due date: 2023-11-09"
    ]

def test_add_item_to_todo_list_due_date_only(manager):
    manager.create_todo_list("Reading")
    assert manager.add_item_to_todo_list("Reading", "Chapter 1", due_date="2023-11-15") == "Item added successfully."
    assert manager.add_item_to_todo_list("Reading", "Chapter 2", due_date="2023-11-22") == "Item added successfully."
    items = manager.show_all_items_in_todo_list("Reading")
    assert items == [
        "Item: Chapter 1, Priority: No priority specified, Due date: 2023-11-15",
        "Item: Chapter 2, Priority: No priority specified, Due date: 2023-11-22"
    ]

def test_add_item_to_nonexistent_todo_list(manager):
    result = manager.add_item_to_todo_list("Supermarket", "Bread")
    assert result == "No TodoList named Supermarket found."
    
def test_add_item_with_invalid_priority(manager):
    manager.create_todo_list("Groceries")
    result_high_priority = manager.add_item_to_todo_list("Groceries", "Milk", priority="High")
    assert result_high_priority == "Priority must be a non-negative integer."
    result_negative_priority = manager.add_item_to_todo_list("Groceries", "Milk", priority=-1)
    assert result_negative_priority == "Priority must be a non-negative integer."

def test_add_item_with_invalid_due_date(manager):
    manager.create_todo_list("Homework")
    result_wrong_format = manager.add_item_to_todo_list("Homework", "Read Chapter 3", due_date="23-11-10")
    assert result_wrong_format == "Due date must be in YYYY-MM-DD format."
    result_invalid_date = manager.add_item_to_todo_list("Homework", "Read Chapter 4", due_date="2023-02-30")
    assert result_invalid_date == "Due date must be in YYYY-MM-DD format."
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Four test functions for show_all_items_in_todo_list function
def test_show_all_items_in_empty_list(manager):
    manager.create_todo_list('EmptyList')
    items = manager.show_all_items_in_todo_list('EmptyList')
    assert items == [], "The item list should be empty for a new todo list."

def test_show_all_items_in_list_with_single_item(manager):
    manager.create_todo_list('SingleItem')
    manager.add_item_to_todo_list('SingleItem', 'Buy milk')
    items = manager.show_all_items_in_todo_list('SingleItem')
    assert items == ['Item: Buy milk, Priority: No priority specified, Due date: No due date'], \
        "The item list should contain a single item with no specified priority or due date."

def test_show_all_items_in_list_with_multiple_items(manager):
    manager.create_todo_list('MultipleItems')
    manager.add_item_to_todo_list('MultipleItems', 'Buy milk', priority=1)
    manager.add_item_to_todo_list('MultipleItems', 'Read book', due_date='2023-11-06')
    items = manager.show_all_items_in_todo_list('MultipleItems')
    assert items == [
        'Item: Buy milk, Priority: 1, Due date: No due date',
        'Item: Read book, Priority: No priority specified, Due date: 2023-11-06'
    ]
    
def test_show_all_items_in_nonexistent_list(manager):
    message = manager.show_all_items_in_todo_list('NonExistentList')
    assert message == "No TodoList named NonExistentList found."
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Three test functions for remove_item_from_todo_list function
def test_remove_item_from_todo_list(manager):
    manager.create_todo_list("Groceries")
    manager.add_item_to_todo_list("Groceries", "Milk")
    result = manager.remove_item_from_todo_list("Groceries", 0)
    assert "Milk" not in manager.show_all_items_in_todo_list("Groceries")
    assert result == "Item at index 0 removed from TodoList Groceries."

def test_remove_item_from_todo_list_invalid_index(manager):
    manager.create_todo_list("Groceries")
    result = manager.remove_item_from_todo_list("Groceries", 0)
    assert result == "Index 0 is out of range for TodoList Groceries."

def test_remove_item_from_nonexistent_list(manager):
    result = manager.remove_item_from_todo_list("Supermarket", 0)
    assert result == "No TodoList named Supermarket found."
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Three test functions for save_to_file function
def test_save_to_file_empty(manager):
    manager.save_to_file()
    assert os.path.exists(manager.filename)
    with open(manager.filename, 'r') as f:
        data = json.load(f)
    assert data == {}
    
def test_save_to_file_with_content(manager):
    manager.create_todo_list('Groceries')
    manager.add_item_to_todo_list('Groceries', 'Breads', priority=1, due_date='2023-11-06')
    manager.save_to_file()
    with open(manager.filename, 'r') as f:
        data = json.load(f)
    assert 'Groceries' in data
    assert data['Groceries'][0]['item'] == 'Breads'

def test_save_to_file_overwrite(manager):
    manager.create_todo_list('OverwriteList')
    manager.save_to_file()
    manager.delete_todo_list('OverwriteList')
    manager.create_todo_list('AnotherList')
    manager.save_to_file()
    with open(manager.filename, 'r') as f:
        data = json.load(f)
    assert 'OverwriteList' not in data
    assert 'AnotherList' in data
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Three test functions for load_from_file function
def test_load_from_empty_file(manager):
    if os.path.exists(manager.filename):
        os.remove(manager.filename)
    with pytest.raises(FileNotFoundError, match=r"The file .* does not exist."):
        manager.load_from_file()
    assert manager.show_all_todo_list() == {}

def test_load_from_valid_data(manager, tmpdir):
    sample_data = {
        "Groceries": [{"item": "Milk", "priority": 1, 'due_date': "2023-11-10"}],
        "Work": [{"item": "Report", "priority": 2, "due_date": "2023-12-21"}],
    }
    filename = tmpdir.join("todo.json")
    with open(str(filename), 'w') as f:
        json.dump(sample_data, f, cls = CustomEncoder)
    manager.load_from_file()
    loaded_data = manager.show_all_todo_list()
    assert len(loaded_data) == 2
    assert "Groceries" in loaded_data and "Work" in loaded_data
    
def test_load_from_invalid_data(manager, tmpdir):
    sample_data = "Not a valid JSON for todo lists"
    filename = tmpdir.join("todo.json")
    with open(str(filename), 'w') as f:
        f.write(sample_data)
    with pytest.raises(Exception):
        manager.load_from_file()
#--------------------------------------------------------------------------------------------

# Another test function for save_to_file and load_from_file both (simulate restarting program)
def test_save_and_load_functionalities(tmpdir):
    file_path = tmpdir.join("todo.json")
    
    manager = TodoListManager(str(file_path))
    manager.create_todo_list('Groceries')
    manager.add_item_to_todo_list('Groceries', 'Apple', due_date="2023-11-10")

    del manager  # Ensure manager is not in scope anymore

    new_manager = TodoListManager(str(file_path))
    assert 'Groceries' in new_manager.show_all_todo_list()
    assert 'Apple' in [item['item'] for item in new_manager.todo_lists['Groceries']]
    assert new_manager.show_all_todo_list()['Groceries'][0]['priority'] == float('inf')