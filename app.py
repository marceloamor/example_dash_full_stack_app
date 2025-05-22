import dash
from dash import html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime

# Import application modules
from config import DASH_TITLE, DEBUG
from database.db import init_db, shutdown_db, db_session
from controllers.todo_controller import TaskController, CategoryController
from views import create_layout
from views.components import task_form, task_list

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://use.fontawesome.com/releases/v5.15.4/css/all.css'
    ],
    title=DASH_TITLE,
    suppress_callback_exceptions=True
)

# Initialize the database
init_db()

# Set the app layout
app.layout = create_layout()

# Define callbacks
@app.callback(
    Output("task-list", "children"),
    [
        Input("refresh-interval", "n_intervals"),
        Input("filter-completed", "checked")
    ]
)
def update_task_list(n_intervals, filter_completed):
    """Update the task list."""
    tasks = TaskController.get_all_tasks()
    return task_list(tasks=tasks, filter_completed=filter_completed).children[2]


@app.callback(
    Output("task-form-container", "children"),
    Output("task-form-container", "style"),
    [Input("add-task-button", "n_clicks")],
    [State("task-form-container", "style")]
)
def toggle_task_form(n_clicks, style):
    """Show or hide the task form."""
    if not n_clicks:
        return dash.no_update, dash.no_update
    
    if style and style.get("display") == "block":
        return dash.no_update, {"display": "none"}
    
    return task_form(), {"display": "block"}


@app.callback(
    Output("task-form-container", "children", allow_duplicate=True),
    [Input({"type": "edit-task", "index": dash.ALL}, "n_clicks")],
    prevent_initial_call=True
)
def edit_task(edit_clicks):
    """Show the task form for editing a task."""
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update
    
    # Get the task ID from the triggered component
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    task_id = int(eval(button_id)["index"])
    
    # Get the task
    task = TaskController.get_task_by_id(task_id)
    if not task:
        return dash.no_update
    
    # Return the task form with the task data
    return task_form(task=task)


@app.callback(
    Output("task-list", "children", allow_duplicate=True),
    [Input("submit-task", "n_clicks")],
    [
        State("task-id", "data"),
        State("title-input", "value"),
        State("description-input", "value"),
        State("due-date-input", "date"),
        State("priority-input", "value"),
        State("category-input", "value")
    ],
    prevent_initial_call=True
)
def submit_task(n_clicks, task_id, title, description, due_date, priority, category_id):
    """Submit a task (create or update)."""
    if not n_clicks or not title:
        return dash.no_update
    
    if task_id:
        # Update existing task
        TaskController.update_task(
            task_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category_id=category_id
        )
    else:
        # Create new task
        TaskController.create_task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category_id=category_id
        )
    
    # Return updated task list
    tasks = TaskController.get_all_tasks()
    return task_list(tasks=tasks).children[2]


@app.callback(
    Output("task-list", "children", allow_duplicate=True),
    [Input({"type": "task-checkbox", "index": dash.ALL}, "checked")],
    [State({"type": "task-checkbox", "index": dash.ALL}, "id")],
    prevent_initial_call=True
)
def toggle_task_completion(checked_values, checkbox_ids):
    """Toggle task completion status."""
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update
    
    # Get the task ID from the triggered component
    checkbox_id = ctx.triggered[0]["prop_id"].split(".")[0]
    task_id = int(eval(checkbox_id)["index"])
    
    # Toggle task completion
    TaskController.toggle_task_completion(task_id)
    
    # Return updated task list
    tasks = TaskController.get_all_tasks()
    return task_list(tasks=tasks).children[2]


@app.callback(
    Output("task-list", "children", allow_duplicate=True),
    [Input({"type": "delete-task", "index": dash.ALL}, "n_clicks")],
    prevent_initial_call=True
)
def delete_task(delete_clicks):
    """Delete a task."""
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update
    
    # Get the task ID from the triggered component
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    task_id = int(eval(button_id)["index"])
    
    # Delete the task
    TaskController.delete_task(task_id)
    
    # Return updated task list
    tasks = TaskController.get_all_tasks()
    return task_list(tasks=tasks).children[2]


@app.callback(
    Output("category-list", "children"),
    [
        Input("add-category-button", "n_clicks"),
        Input({"type": "delete-category", "index": dash.ALL}, "n_clicks")
    ],
    [
        State("category-name-input", "value"),
        State("category-color-input", "value")
    ],
    prevent_initial_call=True
)
def manage_categories(add_clicks, delete_clicks, category_name, category_color):
    """Add or delete categories."""
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update
    
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if triggered_id == "add-category-button" and category_name:
        # Add new category
        CategoryController.create_category(name=category_name, color=category_color)
    else:
        # Check if it's a delete button
        try:
            button_id = eval(triggered_id)
            if button_id.get("type") == "delete-category":
                category_id = button_id.get("index")
                CategoryController.delete_category(category_id)
        except:
            pass
    
    # Get updated categories
    categories = CategoryController.get_all_categories()
    
    # Return updated category list
    if not categories:
        return [
            dbc.ListGroupItem(
                "No categories yet. Add one above!",
                className="text-center font-italic"
            )
        ]
    
    return [
        dbc.ListGroupItem(
            [
                html.Span(
                    cat.name,
                    style={
                        "backgroundColor": cat.color,
                        "color": "white",
                        "padding": "0.25rem 0.5rem",
                        "borderRadius": "0.25rem"
                    }
                ),
                html.Button(
                    html.I(className="fas fa-trash"),
                    id={"type": "delete-category", "index": cat.id},
                    className="btn btn-sm btn-outline-danger float-right",
                    title="Delete Category"
                )
            ],
            id={"type": "category-item", "index": cat.id},
            action=True
        )
        for cat in categories
    ]


@app.callback(
    Output("task-statistics", "children"),
    [Input("refresh-interval", "n_intervals")]
)
def update_statistics(n_intervals):
    """Update task statistics."""
    tasks = TaskController.get_all_tasks()
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.completed)
    pending_tasks = total_tasks - completed_tasks
    
    # Calculate completion rate
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Count tasks by priority
    priority_counts = {1: 0, 2: 0, 3: 0}
    for task in tasks:
        priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1
    
    # Count overdue tasks
    overdue_tasks = sum(1 for task in tasks if task.is_overdue)
    
    return [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Tasks", className="card-title"),
                        html.P(total_tasks, className="statistics-number")
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Completed", className="card-title"),
                        html.P(completed_tasks, className="statistics-number text-success")
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Pending", className="card-title"),
                        html.P(pending_tasks, className="statistics-number text-warning")
                    ])
                ], className="mb-3")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Overdue", className="card-title"),
                        html.P(overdue_tasks, className="statistics-number text-danger")
                    ])
                ], className="mb-3")
            ], width=6)
        ]),
        dbc.Progress(
            value=completion_rate,
            label=f"{completion_rate:.1f}%",
            color="success",
            className="mb-3"
        ),
        html.Div([
            html.P("Tasks by Priority:", className="font-weight-bold"),
            html.Div([
                html.Span(f"High: {priority_counts[3]}", className="badge badge-danger mr-2"),
                html.Span(f"Medium: {priority_counts[2]}", className="badge badge-warning mr-2"),
                html.Span(f"Low: {priority_counts[1]}", className="badge badge-info")
            ])
        ])
    ]


# Shutdown database connection when app is closed
@app.server.teardown_appcontext
def shutdown_session(exception=None):
    shutdown_db()


# Run the app
if __name__ == "__main__":
    app.run_server(debug=DEBUG)
