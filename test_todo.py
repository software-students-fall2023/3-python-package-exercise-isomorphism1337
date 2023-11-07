from todo import TodoListManager
from todo import CustomEncoder
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
# Three test functions for show_all_items_in_todo_list function
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