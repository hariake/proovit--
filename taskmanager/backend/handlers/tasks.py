import json
import jwt
import os
import tornado.web
from db import SessionLocal
from models import Task, TaskStatus

SECRET = os.environ.get("JWT_SECRET", "devsecret")

def get_current_user(self):
    auth_header = self.request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:]  # Remove "Bearer " prefix
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.InvalidTokenError:
        return None
    
class TasksHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json") #sets the default content type for responses to application/json.

    # GET request handler for fetching all tasks of the current user.
    def get(self, task_id=None):
        user_id = get_current_user(self)
        if not user_id: 
            self.set_status(401)
            self.write({"error": "Unauthorized"})
            return # if there is no user_id in the token, return a 401 error with a message indicating that the user is unauthorized
        
        db = SessionLocal()
        try:
            tasks = db.query(Task).all() # gets all tasks that belong to the current user
            self.write({"tasks": [serialize(t) for t in tasks]}) #serializes the tasks python objects into JSON format and returns them in the response
        finally:
            db.close()    

    # POST request handler for creating a new task. 
    def post(self):
        user_id = get_current_user(self)
        if not user_id: 
            self.set_status(401)
            self.write({"error": "Unauthorized"})
            return  # if there is no user_id in the token, return a 401 error with a message indicating that the user is unauthorized
        
        try:
            data = json.loads(self.request.body) #gets the data from the POST request body and try to parse it as JSON. 
        except Exception:
            self.set_status(400)
            self.write({"error": "Invalid JSON"})
            return  # if the parsing fails, return a 400 error with a message indicating that the JSON is invalid  
        
        title = data.get("title") #gets the title from request body
        if not title:
            self.set_status(400)
            self.write({"error": "Title is required"})
            return  # if the title is missing, return a 400 error with a message indicating that the title is required
        
        db = SessionLocal() #opens a new database session
        try:
            task = Task(
                title=title,
                description=data.get("description", ""),
                status=TaskStatus(data.get("status", "todo")),
                deadline=data.get("deadline"),
                user_id=user_id,
                assignee_id=data.get("assignee_id")
            )
            db.add(task) #adds the new task to the database session
            db.commit() #commits the session to save the new task in the database
            db.refresh(task) #refreshes the task object to get the generated id from the database
            self.set_status(201) #HTTP code that something was created successfully
            self.write(serialize(task)) #returns the created task in the response
        finally:
            db.close() #closes the database session    
                

class TaskDetailHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    # GET request handler for fetching a specific task by its id.
    def get(self, task_id):
        user_id = get_current_user(self)
        if not user_id: 
            self.set_status(401)
            self.write({"error": "Unauthorized"})
            return  # if there is no user_id in the token, return a 401 error with a message indicating that the user is unauthorized
        
        db = SessionLocal() #opens a new database session
        try:
            task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first() # gets the task with the specified id that belongs to the current user 
            if not task:
                self.set_status(404)
                self.write({"error": "Task not found"})
                return  # if the task is not found, return a 404 error with a message indicating that the task is not found
            self.write(serialize(task)) #returns the task data in the response
        finally:    
            db.close() #closes the database session        

    # PUT request handler for updating a specific task by its id.
    def put(self, task_id):
        user_id = get_current_user(self)
        if not user_id: 
            self.set_status(401)
            self.write({"error": "Unauthorized"})
            return  # if there is no user_id in the token, return a 401 error with a message indicating that the user is unauthorized

        try:
            data = json.loads(self.request.body) #gets the data from the PUT request body and try to parse it as JSON. 
        except Exception:
            self.set_status(400)
            self.write({"error": "Invalid JSON"})
            return  # if the parsing fails, return a 400 error with a message indicating that the JSON is invalid  
        
        db = SessionLocal() #opens a new database session
        try:
            task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first() # gets the task with the specified id that belongs to the current user 
            if not task:
                self.set_status(404)
                self.write({"error": "Task not found"})
                return  # if the task is not found, return a 404 error with a message indicating that the task is not found
            
            # updates the task fields with the new data from the request body only if there is new data for that field.
            if "title" in data:
                task.title = data["title"]
            if "description" in data:
                task.description = data["description"]
            if "status" in data:
                task.status = TaskStatus(data["status"])
            if "deadline" in data:
                task.deadline = data["deadline"]
            if "assignee_id" in data:
                task.assignee_id = data["assignee_id"]  

            db.commit() #commits the session to save the updated task in the database  
            db.refresh(task) #refreshes the task object to get the updated data from the database
            self.write(serialize(task)) #returns the updated task in the response
        finally:
            db.close() #closes the database session


    def delete(self, task_id):
        user_id = get_current_user(self)
        if not user_id: 
            self.set_status(401)
            self.write({"error": "Unauthorized"})
            return  # if there is no user_id in the token, return a 401 error with a message indicating that the user is unauthorized

        db = SessionLocal() #opens a new database session
        try:
            task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first() # gets the task with the specified id that belongs to the current user 
            if not task:
                self.set_status(404)
                self.write({"error": "Task not found"})
                return  # if the task is not found, return a 404 error with a message indicating that the task is not found
            
            db.delete(task) #deletes the task from the database
            db.commit() #commits the session to save the changes in the database
            self.write({"message": "Task deleted successfully"}) #returns a success message in the response
        finally:
            db.close() #closes the database session


def serialize(task):

    #converts Task python object into a JSON-serializable dictionary format.
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value, #status is an enum, need to get its value to convert it into string.
        "deadline": task.deadline.isoformat() if task.deadline else None,
        "created_at": task.created_at.isoformat() if task.created_at else None, #isoformat converts datetime into string.
        "user_id": task.user_id,
        "assignee_id": task.assignee_id
    }          
                    