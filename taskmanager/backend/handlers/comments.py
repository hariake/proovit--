import json
import jwt
import os
import tornado.web
from db import SessionLocal
from models import Comment, Task

SECRET = os.environ.get("JWT_SECRET", "devsecret")

# Helper function to get the current user id from the JWT token in the Authorization header.
def get_current_user(handler):
    auth_header = handler.request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:]  # Remove "Bearer " prefix
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.InvalidTokenError:
        return None
    

class CommentsHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json") #sets the default content type for responses to application/json.

    def get(self, task_id):
        user_id = get_current_user(self)
        if not user_id: 
            self.set_status(401)
            self.write({"error": "Unauthorized"})
            return  # checks if you are logged in to see the comments
        db = SessionLocal()
        try:
            comments = db.query(Comment).filter(Comment.task_id == task_id).all() # gets all comments that belong to the specified task
            for c in comments:
                _ = c.user # access the user relationship to populate it for serialization, this is needed to get the username of the comment author in the response
            self.write({"comments": [serialize(c) for c in comments]}) #serializes the comments python objects into JSON format and returns them in the response              
        finally:
            db.close()

    def post(self, task_id):
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
        
        body = data.get("content") #gets the body of the comment from request body
        if not body:
            self.set_status(400)
            self.write({"error": "Comment content is required"})
            return  # if the body is missing, return a 400 error with a message indicating that the comment content is required
        
        db = SessionLocal() #opens a new database session
        try:
            comment = Comment(
                content=body,
                task_id=task_id,
                user_id=user_id
            )
            db.add(comment) #adds the new comment to the database session
            db.commit() #commits the session to save the new comment in the database
            db.refresh(comment) #refreshes the comment object to get the generated id from the database
            comment = db.query(Comment).filter(Comment.id == comment.id).first() #query the comment again to get the user relationship populated for serialization
            self.set_status(201) #HTTP code that something was created successfully
            self.write(serialize(comment)) #returns the created comment in the response
        finally:
            db.close() #closes the database session


def serialize(comment):
    return {
        "id": comment.id,
        "body": comment.content,
        "task_id": comment.task_id,
        "user_id": comment.user_id,
        "username": comment.user.username,
        "created_at": comment.created_at.isoformat() if comment.created_at else None,
    }            