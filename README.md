# To-Do App - Full Stack Dash Application

A simple to-do application built with Dash, SQLAlchemy and SQLite. This project demonstrates how to create a full-stack web application using Python with a clean, modular architecture.

## Project Overview

This application is a complete task management system built entirely in Python. It features:

- A responsive web interface built with Dash and Bootstrap
- A SQLite database for data persistence
- SQLAlchemy ORM for database operations
- A clear separation of concerns with Models, Views, and Controllers

## Project Structure

```
example_dash_full_stack_app/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── models/                 # SQLAlchemy data models
│   ├── __init__.py
│   ├── base.py             # Base model with common methods
│   └── todo.py             # To-do specific models
├── database/               # Database connection and setup
│   ├── __init__.py
│   └── db.py               # Database utilities
├── views/                  # Dash layout components
│   ├── __init__.py
│   ├── layout.py           # Main application layout
│   └── components/         # Reusable UI components
│       ├── __init__.py
│       ├── task_form.py    # Task creation/edit form
│       └── task_list.py    # Task list display
├── controllers/            # Business logic
│   ├── __init__.py
│   └── todo_controller.py  # CRUD operations for tasks
├── assets/                 # Static files
│   └── style.css           # Custom CSS
├── requirements.txt        # Project dependencies
└── README.md               # Documentation
```

## Detailed Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Step-by-Step Installation

1. **Clone the Repository**

   Open your terminal (Command Prompt or PowerShell on Windows, Terminal on macOS/Linux) and run:
   ```bash
   git clone https://github.com/yourusername/example_dash_full_stack_app.git
   cd example_dash_full_stack_app
   ```

2. **Create and Activate a Virtual Environment**

   Creating a virtual environment keeps dependencies for different projects separate.

   **On Windows:**
   ```bash
   python -m venv .venv
   venv\Scripts\activate
   ```

   **On macOS/Linux:**
   ```bash
   python -m venv .venv
   source venv/bin/activate
   ```

   You should see `(.venv)` at the beginning of your terminal prompt, indicating the virtual environment is active.

3. **Install Dependencies**

   Install all required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**

   Launch the application:
   ```bash
   python app.py
   ```

   The terminal will display a message like:
   ```
   Dash is running on http://127.0.0.1:8050/
   ```

5. **Access the Application**

   Open your web browser and navigate to:
   ```
   http://127.0.0.1:8050/
   ```

## How to Use the Application

### Managing Tasks

1. **View Tasks**
   - Tasks are displayed in the main panel
   - Tasks show priority level, category (if assigned), and due date
   - Overdue tasks are highlighted

2. **Add a Task**
   - Click "Add New Task" button
   - Fill in the form with task details:
     - Title (required)
     - Description (optional)
     - Due date (optional)
     - Priority (Low, Medium, High)
     - Category (if any exist)
   - Click "Add Task" to save

3. **Edit a Task**
   - Click the edit icon (pencil) next to a task
   - Modify any details in the form
   - Click "Update Task" to save changes

4. **Complete a Task**
   - Check the checkbox next to a task to mark it as complete
   - Completed tasks appear with strikethrough text

5. **Delete a Task**
   - Click the delete icon (trash) next to a task
   - The task will be permanently removed

### Managing Categories

1. **Add a Category**
   - Enter a category name
   - Select a colour using the colour picker
   - Click "Add" to create the category

2. **Delete a Category**
   - Click the delete icon next to a category
   - Note: This will remove the category from all tasks associated with it

## How It Works: Architecture Explanation

### 1. Database Layer

The application uses a SQLite database with SQLAlchemy ORM for data modelling:

- `database/db.py` - Sets up the database connection and session management
- `models/base.py` - Defines a base model class with common functionality
- `models/todo.py` - Defines the Task and Category models

The models define the database schema and relationships:
- A Task can belong to a Category (many-to-one relationship)
- A Category can have multiple Tasks (one-to-many relationship)

### 2. Business Logic Layer (Controllers)

Controllers handle the application's business logic, separating it from the UI:

- `controllers/todo_controller.py` - Contains TaskController and CategoryController classes
- These controllers implement CRUD operations (Create, Read, Update, Delete)
- They handle data validation and processing

### 3. User Interface Layer (Views)

The UI is built with Dash and Bootstrap components:

- `views/layout.py` - Defines the main application layout
- `views/components/` - Contains reusable UI components
  - `task_form.py` - Form for creating and editing tasks
  - `task_list.py` - Display for the list of tasks

### 4. Application Entry Point

- `app.py` - Initialises the Dash application and sets up callbacks
- Callbacks connect user interactions with controller actions

### 5. Configuration

- `config.py` - Contains application settings like database URI and debug mode
- Environment variables can be used to override default settings

## Data Flow

1. User interacts with the UI (e.g., adds a task)
2. A Dash callback is triggered
3. The callback calls the appropriate controller method
4. The controller creates or modifies data using the models
5. The model interacts with the database
6. Updated data is retrieved and passed back to the UI
7. The UI is refreshed to show the changes

## Extending the Application

### Adding New Features

1. **New Data Models**
   - Define new model classes in `models/`
   - Update `database/db.py` to import the models
   - Run the application to create the database tables

2. **New Controllers**
   - Create new controller classes in `controllers/`
   - Implement business logic methods

3. **New UI Components**
   - Create new component files in `views/components/`
   - Update `views/layout.py` to include the new components
   - Add new callbacks in `app.py` to handle interactions

### Moving to a Production Database

To switch from SQLite to another database like PostgreSQL:

1. Install the appropriate database driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `config.py` with the new database URI:
   ```python
   SQLALCHEMY_DATABASE_URI = os.environ.get(
       'DATABASE_URL',
       'postgresql://username:password@localhost:5432/todo_db'
   )
   ```

## Troubleshooting

### Common Issues

1. **Module Not Found Errors**
   - Ensure you've activated your virtual environment
   - Verify all dependencies are installed with `pip list`

2. **Database Errors**
   - Check database file permissions
   - Delete the `todo.db` file and restart to reset the database

3. **UI Not Updating**
   - Clear your browser cache
   - Check for JavaScript errors in the browser console

### Getting Help

If you encounter issues:
1. Check the logs in the terminal where the app is running
2. Read the Dash documentation: https://dash.plotly.com/
3. Consult the SQLAlchemy documentation: https://docs.sqlalchemy.org/

## Learning Resources

- **Dash Documentation**: https://dash.plotly.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Bootstrap Documentation**: https://getbootstrap.com/docs/5.0/

- CRUD operations implementation
