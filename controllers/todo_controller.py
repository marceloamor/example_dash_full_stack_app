from datetime import datetime
from database.db import db_session
from models.todo import Task, Category

class TaskController:
    """Controller for task operations."""
    
    @staticmethod
    def get_all_tasks():
        """Get all tasks."""
        return Task.query.order_by(Task.completed, Task.due_date).all()
    
    @staticmethod
    def get_task_by_id(task_id):
        """Get a task by ID."""
        return Task.get_by_id(task_id)
    
    @staticmethod
    def create_task(title, description=None, due_date=None, priority=2, category_id=None):
        """Create a new task."""
        # Convert due_date string to datetime object if provided
        due_date_obj = None
        if due_date:
            try:
                due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                # Invalid date format
                pass
        
        task = Task(
            title=title,
            description=description,
            due_date=due_date_obj,
            priority=priority,
            category_id=category_id
        )
        task.save(db_session)
        return task
    
    @staticmethod
    def update_task(task_id, **kwargs):
        """Update a task."""
        task = Task.get_by_id(task_id)
        if not task:
            return None
        
        # Convert due_date string to datetime object if provided
        if 'due_date' in kwargs and kwargs['due_date']:
            try:
                kwargs['due_date'] = datetime.strptime(kwargs['due_date'], "%Y-%m-%d")
            except ValueError:
                # Invalid date format
                del kwargs['due_date']
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        task.save(db_session)
        return task
    
    @staticmethod
    def delete_task(task_id):
        """Delete a task."""
        task = Task.get_by_id(task_id)
        if task:
            task.delete(db_session)
            return True
        return False
    
    @staticmethod
    def toggle_task_completion(task_id):
        """Toggle task completion status."""
        task = Task.get_by_id(task_id)
        if task:
            task.completed = not task.completed
            task.save(db_session)
            return task
        return None


class CategoryController:
    """Controller for category operations."""
    
    @staticmethod
    def get_all_categories():
        """Get all categories."""
        return Category.query.order_by(Category.name).all()
    
    @staticmethod
    def get_category_by_id(category_id):
        """Get a category by ID."""
        return Category.get_by_id(category_id)
    
    @staticmethod
    def create_category(name, color="#007BFF"):
        """Create a new category."""
        category = Category(name=name, color=color)
        category.save(db_session)
        return category
    
    @staticmethod
    def update_category(category_id, **kwargs):
        """Update a category."""
        category = Category.get_by_id(category_id)
        if not category:
            return None
        
        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)
        
        category.save(db_session)
        return category
    
    @staticmethod
    def delete_category(category_id):
        """Delete a category."""
        category = Category.get_by_id(category_id)
        if category:
            category.delete(db_session)
            return True
        return False
