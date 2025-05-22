import dash_bootstrap_components as dbc
from dash import html, dcc
import datetime

from controllers.todo_controller import TaskController


def task_list_item(task):
    """
    Create a list item for a single task.
    
    Args:
        task: Task object
    
    Returns:
        A Dash list item component
    """
    # Determine task styling based on completion status
    item_style = {"textDecoration": "line-through", "opacity": "0.7"} if task.completed else {}
    
    # Determine badge color based on priority
    priority_colors = {1: "info", 2: "warning", 3: "danger"}
    priority_color = priority_colors.get(task.priority, "warning")
    
    # Format due date
    due_date_text = ""
    if task.due_date:
        due_date = task.due_date.strftime("%Y-%m-%d")
        
        # Highlight overdue tasks
        if task.is_overdue:
            due_date_text = html.Span(
                f"Due: {due_date} (Overdue)",
                className="text-danger ml-2"
            )
        else:
            due_date_text = html.Span(
                f"Due: {due_date}",
                className="text-muted ml-2"
            )
    
    # Category badge
    category_badge = None
    if task.category:
        category_badge = html.Span(
            task.category.name,
            className="badge rounded-pill",
            style={
                "backgroundColor": task.category.color,
                "color": "white",
                "marginLeft": "0.5rem"
            }
        )
    
    return dbc.ListGroupItem(
        [
            # Checkbox for task completion
            dbc.Checkbox(
                id={"type": "task-checkbox", "index": task.id},
                checked=task.completed,
                className="float-left mr-2"
            ),
            
            # Task title and badges
            html.Div(
                [
                    html.Span(task.title, style=item_style),
                    html.Span(
                        task.priority_label,
                        className=f"badge badge-{priority_color} ml-2"
                    ),
                    category_badge,
                    due_date_text
                ],
                className="d-inline-block"
            ),
            
            # Action buttons
            html.Div(
                [
                    html.Button(
                        html.I(className="fas fa-edit"),
                        id={"type": "edit-task", "index": task.id},
                        className="btn btn-sm btn-outline-primary mr-1",
                        title="Edit Task"
                    ),
                    html.Button(
                        html.I(className="fas fa-trash"),
                        id={"type": "delete-task", "index": task.id},
                        className="btn btn-sm btn-outline-danger",
                        title="Delete Task"
                    )
                ],
                className="float-right"
            ),
            
            # Task description (collapsed by default)
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody(task.description),
                    className="mt-2"
                ),
                id={"type": "task-description", "index": task.id},
                is_open=False
            )
        ],
        id={"type": "task-item", "index": task.id},
        action=True,
        className="d-flex justify-content-between align-items-center"
    )


def task_list(tasks=None, filter_completed=False, category_id=None):
    """
    Create a list of tasks with filtering options.
    
    Args:
        tasks: List of Task objects, if None, fetches all tasks
        filter_completed: Whether to filter out completed tasks
        category_id: Category ID to filter by
    
    Returns:
        A Dash list component
    """
    if tasks is None:
        tasks = TaskController.get_all_tasks()
    
    # Apply filters
    if filter_completed:
        tasks = [task for task in tasks if not task.completed]
    
    if category_id:
        tasks = [task for task in tasks if task.category_id == category_id]
    
    # Create list items
    list_items = [task_list_item(task) for task in tasks]
    
    if not list_items:
        list_items = [
            dbc.ListGroupItem(
                "No tasks found. Add a new task to get started!",
                className="text-center font-italic"
            )
        ]
    
    return html.Div(
        [
            html.H3("Tasks", className="mb-3"),
            
            # Filter controls
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Checkbox(
                                    id="filter-completed",
                                    label="Hide completed tasks",
                                    checked=filter_completed,
                                    className="form-check-input"
                                )
                            ],
                            className="form-check"
                        ),
                        width=6
                    ),
                    dbc.Col(
                        html.Button(
                            "Add New Task",
                            id="add-task-button",
                            className="btn btn-primary float-right"
                        ),
                        width=6,
                        className="text-right"
                    )
                ],
                className="mb-3"
            ),
            
            # Task list
            dbc.ListGroup(list_items, id="task-list")
        ]
    )
