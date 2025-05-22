import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback
import datetime

from controllers.todo_controller import CategoryController


def task_form(task=None, categories=None):
    """
    Create a form for adding or editing a task.
    
    Args:
        task: Task object if editing, None if adding a new task
        categories: List of categories
    
    Returns:
        A Dash form component
    """
    if categories is None:
        categories = CategoryController.get_all_categories()
    
    # Prepare form values based on whether we're editing or adding
    form_title = "Add New Task" if not task else "Edit Task"
    submit_button_text = "Add Task" if not task else "Update Task"
    
    title_value = task.title if task else ""
    description_value = task.description if task and task.description else ""
    due_date_value = task.due_date.date().isoformat() if task and task.due_date else ""
    priority_value = task.priority if task else 2
    category_value = task.category_id if task and task.category_id else None
    
    # Create category options for dropdown
    category_options = [{"label": "No Category", "value": None}]
    category_options.extend([
        {"label": cat.name, "value": cat.id} for cat in categories
    ])
    
    form = dbc.Form([
        html.H4(form_title, className="mb-3"),
        
        # Task ID (hidden if editing)
        dcc.Store(id="task-id", data=task.id if task else None),
        
        # Title
        dbc.Row([
            dbc.Col([
                dbc.Label("Title", html_for="title-input"),
                dbc.Input(
                    id="title-input",
                    type="text",
                    placeholder="Enter task title",
                    value=title_value,
                    required=True
                ),
            ]),
        ], className="mb-3"),
        
        # Description
        dbc.Row([
            dbc.Col([
                dbc.Label("Description", html_for="description-input"),
                dbc.Textarea(
                    id="description-input",
                    placeholder="Enter task description (optional)",
                    value=description_value,
                    style={"height": "100px"}
                ),
            ]),
        ], className="mb-3"),
        
        # Due Date
        dbc.Row([
            dbc.Col([
                dbc.Label("Due Date", html_for="due-date-input"),
                dcc.DatePickerSingle(
                    id="due-date-input",
                    min_date_allowed=datetime.date.today(),
                    date=due_date_value or None,
                    placeholder="Select due date (optional)",
                    display_format="YYYY-MM-DD",
                    className="w-100"
                ),
            ]),
        ], className="mb-3"),
        
        # Priority
        dbc.Row([
            dbc.Col([
                dbc.Label("Priority", html_for="priority-input"),
                dbc.Select(
                    id="priority-input",
                    options=[
                        {"label": "Low", "value": 1},
                        {"label": "Medium", "value": 2},
                        {"label": "High", "value": 3}
                    ],
                    value=priority_value
                ),
            ]),
        ], className="mb-3"),
        
        # Category
        dbc.Row([
            dbc.Col([
                dbc.Label("Category", html_for="category-input"),
                dbc.Select(
                    id="category-input",
                    options=category_options,
                    value=category_value
                ),
            ]),
        ], className="mb-3"),
        
        # Submit and Cancel buttons
        dbc.ButtonGroup([
            dbc.Button(
                submit_button_text,
                id="submit-task",
                color="primary",
                type="submit"
            ),
            dbc.Button(
                "Cancel",
                id="cancel-task",
                color="secondary",
                className="ms-2"
            )
        ], className="mt-3 d-flex justify-content-end")
    ])
    
    return form
