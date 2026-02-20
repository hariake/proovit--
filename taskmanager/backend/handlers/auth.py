import json
import jwt
import bcrypt
import os
import tornado.web
from db import SessionLocal
from models import User

SECRET = os.environ.get("JWT_SECRET", "devsecret")

# Registration handler for creating a new account with username and password.

class RegisterHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    #get the data from the request body and try to parse it as JSON. if the parsing fails, return a 400 error with a message indicating that the JSON is invalid

    def post(self):
        try:
            data = json.loads(self.request.body)
        except Exception:
            self.set_status(400)
            self.write(json.dumps({"error": "Invalid JSON"}))
            return        

        username = data.get("username") #gets the username from request body
        password = data.get("password") #get the password from request body

        # if username or password is missing, return a 400 error with a message indicating that both fields are required

        if not username or not password:
            self.set_status(400)
            self.write(json.dumps({"error": "Username and password are required"}))
            return
        
        db = SessionLocal() #opens a new database session
        try:
            existing_user = db.query(User).filter_by(username=username).first() 

            if existing_user:
                self.set_status(409)
                self.write({"error": "Username already exists"})
                return
            
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) #hashes the password using bcrypt
            user = User(
                username=username, 
                password_hash=hashed.decode() #stores the hashed password in the database
            )
            db.add(user) #adds the new user to the database session
            db.commit() #commits the session to save the new user in the database
            db.refresh(user) #refreshes the user object to get the generated id from the database
            self.set_status(201) #HTTP code that something was created successfully
            self.write({"message": "User registered successfully", "user_id": user.id}) #returns a success message with the new user's id

        finally:
                db.close() #closes the database session

# Login handler for logging in with existing username and password.

class LoginHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    def post(self):
        try:
            data = json.loads(self.request.body)
        except Exception:
            self.set_status(400)
            self.write({"error": "Invalid JSON"})
            return
        
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            self.set_status(400)
            self.write({"error": "Username and password are required"})
            return
        
        db = SessionLocal()
        try:
            user = db.query(User).filter_by(username=username).first()

            if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                self.set_status(401)
                self.write({"error": "Invalid username or password"})
                return
            
            token = jwt.encode(
                {"user_id": user.id, "username": user.username},
                SECRET,
                algorithm="HS256"
            )

            self.write({
                "token": token,
                "user_id": user.id,
                "username": user.username
            })

        finally:
            db.close()