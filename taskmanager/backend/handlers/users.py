import tornado.web
from db import SessionLocal
from models import User


class UsersHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    # GET request handler for getting all users.
    def get(self):
        db = SessionLocal() #opens a new database session
        try:
            users = db.query(User).all() # gets all users from the database
            self.write({"users": [
                {
                    "id": u.id,
                    "username": u.username,
                }
                for u in users # creates a list containing the id and username of each user and returns it in the response
            ]})
        finally:
            db.close() #closes the database session
    