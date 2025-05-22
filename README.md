# To-Do App - Full Stack Dash Application

A simple to-do application built with Dash, SQLAlchemy and SQLite. This project demonstrates how to create a full-stack web application using Python.

## Project Structure

- `app.py`: Main application entry point
- `models/`: SQLAlchemy data models
- `database/`: Database connection and setup
- `views/`: Dash layout components
- `controllers/`: Business logic
- `assets/`: Static files (CSS, images)

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd example_dash_full_stack_app
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:8050/
   ```

## Features

- Create, read, update, and delete tasks
- Organise tasks by categories
- Set priorities and due dates
- Mark tasks as complete
- Filter and sort tasks

## Development

This project is designed as a learning resource for beginners to understand:
- Dash framework for web applications
- SQLAlchemy ORM for database operations
- Full-stack application architecture
- CRUD operations implementation
