# How to Use and Contribute to the `todopkg` Package

## For Developers: Using `todopkg`

### Installing `todopkg`

To install `todopkg`, run:

```bash
pip install todopkg
```

### Documentation and Examples

The `todopkg` provides a simple interface for managing a to-do list. Here's a quick documentation on how to use it:

- **Create a to-do list instance:**

  ```python
  from todo import TodoListManager
  todo_manager = TodoListManager()
  ```

- **Create a new to-do list**

  ```python
  todo_manager.create_todo_list('Groceries')
  ```

- **Add items to the to-do list:**

  ```python
  todo_manager.add_item_to_todo_list('Groceries', 'Apples')
  ```

- **Remove items from the to-do list:**

  ```python
  todo_manager.remove_item_from_todo_list('Groceries', 0)
  ```

- **Update to-do list name:**

  ```python
  todo_manager.change_todo_list_name('Groceries', 'Supermarket')
  ```

- **Delete to-do list:**

  ```python
  todo_manager.delete_todo_list('Supermarket')
  ```

- **Show all to-do list:**

  ```python
  todo_manager.show_all_todo_list()
  ```

  

### Example Program

For a full example program that utilizes all functionalities, refer to [Example TodoList Usage](https://github.com/yourusername/todopkg/example.py).

---

## For Contributors: Setting Up the Development Environment

### Prerequisites

- Python 3.9+
- pipenv
- pytest
- build
- twine

### Initial Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/software-students-fall2023/3-python-package-exercise-isomorphism1337.git
   cd 3-python-package-exercise-isomorphism1337
   ```

2. Install the dependencies using `pipenv`:

   ```bash
   pipenv install --dev
   ```

### Running Tests

To run tests and verify everything is working as expected:

```bash
pipenv run pytest
```

### Building the Package

After making changes, you can build the package locally to test:

```bash
pipenv run python -m build
```

This will create distribution files in the `dist` directory.

### Uploading to PyPI

To upload the package to PyPI (after setting up your credentials):

```bash
pipenv run twine upload dist/*
```

**Note:** Use TestPyPI to test your package deployment before uploading to the main PyPI repository.

