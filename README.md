# To Do List RESTful API using FastAPI

This is a simple RESTful API for managing a To-Do List application built with FastAPI and SQLite. The API allows users to create, read, update, and delete to-do items.

## Features

- Create a new to-do item
- Retrieve all to-do items
- Retrieve a specific to-do item by ID
- Update a specific to-do item by ID
- Delete a specific to-do item by ID

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sprnjt/todolist.git
   cd todolist
   ```

2. Create a virtual environment (optional):

   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```

3. Install the required packages:

   ```bash
   pip install fastapi uvicorn
   ```

### Running the Application

1. Initialize the database (this is done automatically when you run the app for the first time).
2. Start the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

3. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation (Swagger UI).

## API Endpoints

### 1. Get All To-Do Items

- **Endpoint**: `GET /todos`
- **Response**: List of to-do items.

### 2. Create a New To-Do Item

- **Endpoint**: `POST /todos`
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "completed": false
  }
  ```
- **Response**: The created to-do item with its ID.

### 3. Get a Specific To-Do Item

- **Endpoint**: `GET /todos/{todo_id}`
- **Response**: The to-do item with the specified ID.

### 4. Update a Specific To-Do Item

- **Endpoint**: `PUT /todos/{todo_id}`
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "completed": false
  }
  ```
- **Response**: The updated to-do item.

### 5. Delete a Specific To-Do Item

- **Endpoint**: `DELETE /todos/{todo_id}`
- **Response**: Confirmation message.

## Error Handling

The API returns appropriate HTTP status codes for different scenarios, including:

- `200 OK`: Successful requests.
- `404 Not Found`: When a to-do item is not found.
- `422 Unprocessable Entity`: When validation errors occur.
