from ..extensions import db  # SQLAlchemy instance to interact with the database
from ..models.todo_model import Todo     # Todo model from SQLAlchemy
from sqlalchemy.exc import OperationalError, SQLAlchemyError 


# -------------------------------
# Create a new todo
# -------------------------------
def create_todo_service(data, user_id):
    """
    Creates a new todo for a specific user.
    Args:
        data (dict): Contains 'title' of the todo
        user_id (int): ID of the user creating the todo
    Returns:
        dict: Serialized todo
        int: HTTP status code 201 (Created)
    """
    try:
        title = data["title"]  # Extract title from request data
        todo = Todo(title=title, user_id=user_id)  # Create Todo instance
        if "completed" in data:
            todo.completed = data["completed"]
        if "description" in data:
            todo.description=data["description"]

        
        db.session.add(todo)    # Add to SQLAlchemy session
        db.session.commit()     # Commit to save in database
        return todo.to_dict(), 201  # Return todo as dictionary with HTTP 201
    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError:
        db.session.rollback()
        return {"error": "Error saving todo"}, 500


# -------------------------------
# List all todos for a user
# -------------------------------
def list_todos_service(user_id):
    """
    Retrieves all todos for a specific user.
    Args:
        user_id (int): ID of the user
    Returns:
        list: List of serialized todos
        int: HTTP status code 200 (OK)
    """
    try:
        todos = Todo.query.filter_by(user_id=user_id, status=True).all()  # Fetch all todos for user
        return [t.to_dict() for t in todos], 200  # Convert each todo to dict and return
    except OperationalError:
        return {"error": "Database unavailable"}, 503
    except SQLAlchemyError:
        return {"error": "Database query failed"}, 500
# -------------------------------
# Get a single todo by ID for a user
# -------------------------------
def get_todo_service(todo_id, user_id):
    """
    Retrieves a specific todo by ID for a user.
    Args:
        todo_id (int): ID of the todo
        user_id (int): ID of the user
    Returns:
        dict: Serialized todo or error message
        int: HTTP status code
    """
    
    try:
        
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id, status=True).first()  # Fetch todo
        print(todo)
        if not todo:
            return {"error": "Todo not found"}, 404  # Return 404 if not found
        
        return todo.to_dict(), 200  # Return todo as dict
    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError as err:
        return {"error": err.message}, 500

# -------------------------------
# Update a todo
# -------------------------------
def update_todo_service(todo_id, data, user_id):
    """
    Updates fields of a todo for a user.
    Args:
        todo_id (int): ID of the todo
        data (dict): Fields to update ('title', 'completed')
        user_id (int): ID of the user
    Returns:
        dict: Updated todo or error message
        int: HTTP status code
    """

    try:
        
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id, status=True).first()  # Fetch todo
        if not todo:
            return {"error": "Todo not found"}, 404  # Return 404 if not found

        # Update only fields provided
        if "title" in data:
            todo.title = data["title"]
        if "completed" in data:
            todo.completed = data["completed"]
        if "description" in data:
            todo.description=data["description"]

        db.session.commit()  # Save changes
        return todo.to_dict(), 200  # Return updated todo

    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError:
        db.session.rollback()
        return {"error": "Error saving todo"}, 500

# -------------------------------
# Delete a todo
# -------------------------------
def delete_todo_service(todo_id, user_id):
    """
    Deletes a todo by ID for a specific user.
    Args:
        todo_id (int): ID of the todo
        user_id (int): ID of the user
    Returns:
        dict: Success or error message
        int: HTTP status code
    """
    try:
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()  # Fetch todo
        if not todo:
            return {"error": "Todo not found"}, 404  # Return 404 if not found

        todo.status=False
        
        # db.session.delete(todo)  # Delete todo from session
        db.session.commit()      # Commit deletion
        return {"message": "Todo deleted"}, 200  # Return success message
    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError as err:
        return {"error": err.message}, 500