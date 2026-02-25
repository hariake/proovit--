# Task Manager

A Lightweight taskmanager built with Python/Tornado, PostgreSQL and React

## Features

 +++ User Registration and login 
 +++ Create, edit and delete tasks with multiple forms of data 
 +++ Drag and drop task dashboard 
 +++ Filter tasks by: My tasks, All tasks, Done tasks 
 +++ Comment on tasks 

 ## Tech Stack

 **Backend:** Python, Tornado, SQLAlchemy, PostgreSQL, Alembic
 **Frontend:** React, TypeScript, Vite, Tailwind CSS
 **infra:** Docker, Docker Compose, Nginx

 ## Requirements

 +++ Docker 
 +++ Python 3.11+ 
 +++ Node.js 20+ 

 ## How to run the app

 1. Clone the repo
```bash
   git clone https://github.com/hariake/proovit--.git
   cd proovit--/taskmanager
```
2. Create env files
```bash
   cp .env.example .env
   cp backend/.env.example backend/.env
```
3. Start the database
```bash
   docker compose up db -d
```
4. Run the backend  **Note:** On Mac/Linux you may need to use `python3` and `pip3` instead of `python` and `pip`
```bash
cd backend
pip install -r requirements.txt
python -m alembic upgrade head
python main.py
```

5. Run the frontend
```bash
cd frontend
npm install
npm run dev
``` 

6. Seed the database (optional)
```bash
cd backend
python seed.py
```
7. Open the app
go to http://localhost:5173 in your browser (default vite port, if you have other apps running vite will give you the next port. See the terminal)

8. Register an account and start creating tasks

## Stop the app
```bash
docker compse down
```

## Wipe the database
```bash
docker compose down -v
```

## API Documentation

- Authentication

``` POST /api/auth/register ```
Register a new User

Request Body:
```
{
    "username" : "joonas",
    "password": "lumi"
}
```
```Response: 201```
```
{
    "message": "User registered successfully",
    "user_id" : 1
}
```
``` POST /api/auth/login ```
Login and get a JWT token

Request Body:
```
{
    "username": "joonas",
    "password": "lumi"
}
```
``` Response: 200 ```
```
{
    "token": "eyJ...",
    "user_id": 1,
    "username": "joonas"
}
```

- Tasks
- All task endpoints require ```Authorization: Bearer <token>``` header

``` GET /api/tasks ```
Get all tasks.
``` Response: 200 ```
```
{
    "tasks": [
        {
            "id": 1,
            "title": "fix a bug in the code",
            "description": "fix the nasty bug in the code",
            "status": "todo",
            "deadline": "2026-03-01T00:00:00+00:00",
            "created_at": "2026-02-25T10:00:00+00:00",
            "user_id": 1,
            "assignee_id": 2
        }
    ]
}
```

``` POST /api/tasks ```
Create a new task
Request Body:`
``` 
{
    "title:" "Fix the bug",
    "description": "Fix the taskCard dragging bug",
    "status": "todo",
    "deadline": "2026-03-01",
    "assignee_id": 5
}
```
```Response: 201 - returns the created task object. ```

``` GET /api/tasks/:id ```
Get a single task by id.
``` Response: 200 - returns the task object. ``` 

``` PUT /api/tasks/:id ```
Update a task. Only the creator or assignee can update a task.
Request Body (all the fields are optional for updating):
``` 
{
    "title": "going to fix the bug",
    "description": "im going to fix the bug assigned to me",
    "status": "being_done",
    "deadline": "2026-03-01",
    "assignee_id" 5
}
```
 ``` response: 200 - returns the updated task object.``` ``` Error 403(forbiden) if not the creator or assignee of the task ```

``` DELETE /api/tasks/:id ```
Delete a task. Only the creator or assignee can delete a task.
``` Response: 200 ``` 
```
{
    "message": "Task deleted successfully"
}
```
``` Error 403(forbidden) if not the creator or assignee of the task ``` 

- Comments
- All comment endpoints require ```Authorization: Bearer <token>``` header.

``` GET /api/tasks/:id/comments ``` 
Get all comments for a task.
``` response: 200 ```
```
{
    "comments": [
        {
            "id": 12,
            "body": "good fixing!",
            "task:_id": 23,
            "used:id": 4,
            "username": "jaanus",
            "created_at": "2026-02-25T10:00:00+00:00"
        }
    ]
}
```
``` POST /api/tasks/:id/comments ```
Add a comment to a task.
```
Request Body:
{
    "content": "Bug fixing rules!"
}
```
``` Response: 201 - returns the created comment object. ``` 

- Users

``` GET /api/users ```
Get all users ( neccessary for assignee dropdown menu). Requires authentication
``` Response: 200 ```
```
{
    "users": [
        {
            "id": 77,
            "username": "veroonika"
        }
    ]
}
```

- All the status codes used
```
200 - OK
201 - Created
304 - Not Modified (data unchanged use cached version)
400 - Bad Request (Bad JSON or missing some fields)
401 - Unautohrized (token is missing or not valid)
403 - Forbidden (not the creator or assignee)
404 - Not Found
500 - Internal Server Error
```