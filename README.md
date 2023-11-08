# Python Package Exercise
# todopkg
[![CI / CD](https://github.com/software-students-fall2023/3-python-package-exercise-isomorphism1337/actions/workflows/main.yml/badge.svg)](https://github.com/software-students-fall2023/3-python-package-exercise-isomorphism1337/actions/workflows/main.yml)
![PyPI](https://img.shields.io/pypi/v/todopkg.svg)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)

`todopkg` is a Python package for managing and organizing to-do lists with prioritization and due dates. This package allows for easy creation, modification, and deletion of to-do lists and tasks.

## Features

- Create multiple to-do lists
- Add tasks with optional priority and due date
- Modify list names
- Delete tasks and lists
- Save and load lists from a file
- Command-line friendly display with table formatting

## PyPI
Click [Here](https://pypi.org/project/todopkg/) to view `todopkg` on PyPI.

## How to Use `todopkg`

### Installing Python

Please make sure you have Python 3.9 or above on your local machine, you can get the latest Python from its [official website](https://www.python.org/).

### Installing `todopkg`

To install `todopkg` via pip, run:

```bash
pip install todopkg
```

### Import `todopkg`

After installing `todopkg`, you can import `todopkg` to your program using:

  ```python
  from todopkg import TodoListManager
  ```

### Documentation and Instruction

- **Create a to-do list instance:**

  When you instantiate the manager, you have the option to specify the filename for saving and loading your to-do lists, as well as control the auto-restore feature that automatically loads existing to-do lists at startup.

  `filename`: This optional parameter allows you to specify the name and path of the file where your to-do lists will be saved (it needs to be a json file). By default, it is set to 'todolist.json'.

  `enable_auto_restore`: Also optional, this flag lets you decide whether to automatically load the to-do lists from the specified file when the manager is created. It is enabled by default.

  - **Default:**

    ```python
    todo_manager = TodoListManager()
    ```

  - **Use custom storage file:**

    ```python
    todo_manager = TodoListManager(filename = my_file.json)
    ```
  - **Disable auto restore:**

    ```python
    todo_manager = TodoListManager(enable_auto_restore = False)
    ```
  - **Use custom storage file and Disable auto restore:**

    ```python
    todo_manager = TodoListManager(filename = my_file.json, enable_auto_restore = False)
    ```

- **Create a new to-do list:**

  Different to-do lists need to have distinct names.

  **Create a to-do list named 'Groceries':**
  ```python
  todo_manager.create_todo_list('Groceries')
  ```
  **Create another to-do list named 'Homeworks':**
  ```python
  todo_manager.create_todo_list('Homeworks')
  ```
- **Add items to the to-do list:**

  To add an item to your to-do list, you'll use the `add_item_to_todo_list` function. You need to specify the name of the list and the item you wish to add.  Items may be assigned a priority level (`int`) or a due date (`YYYY-MM-DD`), or both, and will be displayed in sorted order accordingly. When both are specified, priority ranking takes precedence over the due date.
  - **Without priority or due date:**

    ```python
    todo_manager.add_item_to_todo_list('Groceries', 'Apples')
    ```
  - **With priority only (the lower the number, the higher the priority):**

    ```python
    todo_manager.add_item_to_todo_list('Homeworks', 'Midterm Review', priority=1)
    ```
  - **With due date only (due date in format "YYYY-MM-DD"):**

    ```python
    todo_manager.add_item_to_todo_list('Homeworks', 'Essay', due_date="2023-11-10")
    ```
  - **With both priority and due date:**

    ```python
    todo_manager.add_item_to_todo_list('Homeworks', 'Essay', priority=2, due_date="2023-11-10")
    ```
- **Remove items from the to-do list:**
  
  To remove an item, you need to specify the list name and the index of the item using `remove_item_from_todo_list` function. Indexing starts at 0, so to remove the first item, you would use index 0.
  ```python
  todo_manager.remove_item_from_todo_list('Groceries', 0)
  ```

- **Update to-do list name:**

  If you need to rename a to-do list, provide the current name followed by the new name to the `change_todo_list_name` function.

  ```python
  todo_manager.change_todo_list_name('Groceries', 'Supermarket')
  ```

- **Delete to-do list:**

  To completely remove a to-do list, simply provide the name of the list to the `delete_todo_list` function.
  ```python
  todo_manager.delete_todo_list('Supermarket')
  ```

- **Show all to-do list:**

  The `show_all_todo_list` function returns a dictionary containing all to-do lists with their items. Each key in the dictionary is a list name, and its value is a list of tasks.

  ```python
  todo_manager.show_all_todo_list()
  ```

  You can manipulate this dictionary however you like to integrate with your application. It provides a 'raw' format for advanced usage and flexibility.

- **Print all to-do lists:**

  The `print_all_todo_lists` function provides a nicely formatted table output to the console for one or all of your to-do lists. You can either print all lists or specify a single list to print by name.

  - **print all to-do lists:**

    ```python
    todo_manager.print_all_todo_lists()
    ```
  - **print a specific to-do list:**
    ```python
    todo_manager.print_all_todo_lists(list_name = 'Groceries')
    ```
- **Displaying all items in a to-do list:**

  To view all the items within a specific to-do list in a formatted, readable manner, you can use the `show_all_items_in_todo_list` function, pass the list's name as the parameter.

  ```python
  todo_manager.show_all_items_in_todo_list('Groceries')
  ```
- **Save to-do lists to a JSON file:**

  Save your to-do lists to a JSON file specified at the beginning using the `save_to_file` function. This functions is invoked automatically before program exit.

  ```python
  todo_manager.save_to_file()
  ```
- **Load to-do lists from a JSON file:**

  Restore your to-do lists from a JSON file specified at the beginning using `load_from_file` function. This function is automatically invoked upon instantiation of `TodoListManager` if `enable_auto_restore` is `True`.

  ```python
  todo_manager.load_from_file()
  ```

### Example Program

For a full example program that utilizes all functionalities, kindly refer to [Example TodoList Usage](./src/todopkg/__main__.py). 

You can also run this file following this procedure:
1. Clone the repository:

   ```bash
   git clone https://github.com/software-students-fall2023/3-python-package-exercise-isomorphism1337.git
   cd 3-python-package-exercise-isomorphism1337
   ```

2. Install `pipenv` if you don't have one on your machine:
    ```bash
    pip install pipenv
    ```

3. Install the dependencies:

    ```bash
    pipenv install --dev
    pipenv shell
    ```
4. Run the example file:

    ```bash
    python -m src.todopkg
    ```

---

## How to contribute to `todopkg`

### Prerequisites

- Python 3.9+

### Initial Setup

1. Clone the repository and cd to the project root directory:

   ```bash
   git clone https://github.com/software-students-fall2023/3-python-package-exercise-isomorphism1337.git
   ```

   ```bash
   cd You_Own_Directory/3-python-package-exercise-isomorphism1337
   ```

2. Install `pipenv` if you don't have one on your machine:

    ```bash
    pip install pipenv
    ```

3. Install the dependencies:

    ```bash
    pipenv install --dev
    pipenv shell
    ```

### Making Changes
1. Create a new branch for your feature or fix:
    ```bash
    git checkout -b your-branch-name
    ```
2. Make your changes to the codebase. Remember to adhere to the       project's coding standards and guidelines.
3. If you've added new code, consider writing tests that cover your changes in the [tests](./tests/) folder. This is important to ensure that your code works as expected and future changes don't break your implementation.

### Running Tests

After making changes, run all tests to ensure that your changes don't break any existing functionality:

  ```bash
  pipenv run pytest
  ```

### Commiting Your Changes

Add your changes to staging, then commit your changes with a descriptive message:

  ```bash
  git add .
  ```
  ```bash
  git commit -m "Your detailed description of the changes"
  ```

### Pushing Changes

Push your changes to your branch:
  ```bash
  git push origin your-branch-name
  ```

### Submitting a Pull Request
Create a new pull request for your branch, and we will review your code later.

### After Your Pull Request is Merged

1. Pull the changes from the original repository:
    ```bash
    git checkout main
    git pull origin main
    ```
2. Delete your old branch:
    ```bash
    git branch -d your-branch-name
    git push origin --delete your-branch-name
    ```

# Contributors

- [Fuzhen Li](https://github.com/fzfzlfz)
- [Jiasheng wang](https://github.com/isomorphismss)
- [Xuefeng Song](https://github.com/wowwowooo)
- [Yuantian Tan](https://github.com/AsukaTan)

