from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import JSONResponse
#IMPORTING THE DEPENDENCIES 
from database import get_db_connection, init_db  # IMPORTING THE DATABASE CONNECTION AND INITIALIZATION 

app = FastAPI()  #CREATING THE FASTAPI INSTANCE

# DATA MODEL FOR THE TO-DO ITEMS    
class TodoItem(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# RESPONSE MODEL FOR THE SUCCESSFUL UPDATE AND CREATION
class TodoItemResponse(TodoItem):
    id: int

# INITIALIZING THE DATABASE
init_db()

# GETTING ALL THE TO-DO ITEMS FROM THE DATABASE 
@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    """Retrieve a list of all to-do items."""
    with get_db_connection() as conn:
        todos = conn.execute('SELECT * FROM todos').fetchall()
    return [dict(todo) for todo in todos]


# CREATING A NEW TO-DO ITEM IN THE DATABASE     
@app.post("/todos", response_model=TodoItemResponse)
def create_todo(todo: TodoItem):
    """Create a new to-do item."""
    with get_db_connection() as conn:
        cursor = conn.execute('INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)',
                               (todo.title, todo.description, todo.completed))
        conn.commit()
    return {**todo.dict(), "id": cursor.lastrowid}

# GETTING A SPECIFIC TO-DO ITEM FROM THE DATABASE BY ITS ID
@app.get("/todos/{todo_id}", response_model=TodoItemResponse)
def get_todo(todo_id: int):
    """Retrieve a specific to-do item by its ID."""
    with get_db_connection() as conn:
        todo = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return dict(todo)

# UPDATING A SPECIFIC TO-DO ITEM IN THE DATABASE BY ITS ID
@app.put("/todos/{todo_id}", response_model=TodoItemResponse, status_code=status.HTTP_200_OK)
def update_todo(todo_id: int, todo: TodoItem):
    """Update a specific to-do item by its ID."""
    with get_db_connection() as conn:
        cursor = conn.execute('UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?',
                               (todo.title, todo.description, todo.completed, todo_id))
        conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {**todo.dict(), "id": todo_id}

# DELETING A SPECIFIC TO-DO ITEM FROM THE DATABASE BY ITS ID
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a specific to-do item by its ID."""
    with get_db_connection() as conn:
        cursor = conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted"}

# HANDLING THE VALIDATION ERRORS
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
