import dash_bootstrap_components as dbc
from dash import html, dcc

from views.components import task_list, task_form
from controllers.todo_controller import CategoryController


def create_layout():
    """Create the main application layout."""
    categories = CategoryController.get_all_categories()
    
    return dbc.Container(
        [
            # Header
            html.Div(
                [
                    html.H1("To-Do App", className="display-4"),
                    html.P(
                        "A simple task management application",
                        className="lead"
                    ),
                    html.Hr(className="my-4")
                ],
                className="jumbotron py-4 mb-4"
            ),
            
            # Main content
            dbc.Row(
                [
                    # Task list
                    dbc.Col(
                        task_list(),
                        md=8
                    ),
                    
                    # Sidebar
                    dbc.Col(
                        [
                            # Task form (initially hidden)
                            html.Div(
                                id="task-form-container",
                                style={"display": "none"}
                            ),
                            
                            # Categories section
                            html.Div(
                                [
                                    html.H4("Categories", className="mb-3"),
                                    
                                    # Add category form
                                    dbc.Form(
                                        [
                                            dbc.FormGroup(
                                                [
                                                    dbc.Input(
                                                        id="category-name-input",
                                                        type="text",
                                                        placeholder="New category name"
                                                    ),
                                                    dbc.Input(
                                                        id="category-color-input",
                                                        type="color",
                                                        value="#007BFF",
                                                        className="ml-2",
                                                        style={"width": "50px"}
                                                    ),
                                                    dbc.Button(
                                                        "Add",
                                                        id="add-category-button",
                                                        color="primary",
                                                        className="ml-2"
                                                    )
                                                ],
                                                className="d-flex"
                                            )
                                        ],
                                        className="mb-3"
                                    ),
                                    
                                    # Category list
                                    dbc.ListGroup(
                                        [
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
                                        ] if categories else [
                                            dbc.ListGroupItem(
                                                "No categories yet. Add one above!",
                                                className="text-center font-italic"
                                            )
                                        ],
                                        id="category-list"
                                    )
                                ],
                                className="mt-4"
                            ),
                            
                            # Statistics section
                            html.Div(
                                [
                                    html.H4("Statistics", className="mb-3"),
                                    html.Div(id="task-statistics")
                                ],
                                className="mt-4"
                            )
                        ],
                        md=4
                    )
                ]
            ),
            
            # Footer
            html.Footer(
                html.P(
                    "To-Do App - A Full Stack Dash Application",
                    className="text-center text-muted"
                ),
                className="mt-4 pt-3 border-top"
            ),
            
            # Stores for app state
            dcc.Store(id="app-state"),
            
            # Interval for refreshing data
            dcc.Interval(
                id="refresh-interval",
                interval=30000,  # 30 seconds
                n_intervals=0
            )
        ],
        fluid=True,
        className="py-3"
    )
