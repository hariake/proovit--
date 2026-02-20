import os
import tornado.ioloop
import tornado.web
from sqlalchemy import text
from db import engine, SessionLocal
from models import Base
from handlers.auth import RegisterHandler, LoginHandler
from handlers.tasks import TasksHandler, TaskDetailHandler

# DATABASE_URL = os.environ.get("DATABASE_URL")
# engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine) #creates tables into DB if they dont exist yet.

# Health check handler that does simplest query to the database to check if the connection is working. 

class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        self.write({"status": "ok", "db": "connected"})     # if the database connection is successful, it will return a JSON response indicating that the status is "ok" and the database is "connected". otherwise will return a error 500 page
            
def make_app():
    return tornado.web.Application([
        (r"/health", HealthHandler),
        (r"/api/auth/register", RegisterHandler),
        (r"/api/auth/login", LoginHandler),
        (r"/api/tasks", TasksHandler),
        (r"/api/tasks/(\d+)", TaskDetailHandler),
    ], debug=True) #debug mode for better error messages and auto reload during development

if __name__ == "__main__":
    app = make_app()
    app.listen(8888, address="0.0.0.0") #address needed for different containers to access the server
    print("Server is running on port 8888")
    tornado.ioloop.IOLoop.current().start()