from dotenv import load_dotenv
load_dotenv() #loads enviroment variables from .env file

from db import SessionLocal
from models import User, Task, Comment, TaskStatus
import bcrypt

def seed():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(User).count() > 0:
            print("Database already seeded.")
            return
        
        print("Seeding database with initial data...")

        # Create users
        users = [
            User(username="joonas",
                 password_hash=bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode()
                ),
            User(username="veroonika",
                 password_hash=bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode()
                 ),
            User(username="jaanus",
                 password_hash=bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode()
                 ),
        ]

        for user in users:
            db.add(user)
        db.commit()
        for user in users:
            db.refresh(user)

        joonas, veroonika, jaanus = users

        print(f"Created users: joonas, veroonika, jaanus (password: password123)")

        # Create tasks
        tasks = [
            Task(
                title="Fix the TaskCard dragging issue",
                description="The TaskCard component is not dragging properly.",
                status=TaskStatus.todo,
                user_id=joonas.id,
                assignee_id=veroonika.id,
            ),
            Task(
                title="Finish README documentation",
                description="Complete the README file with setup instructions and API documentation.",
                status=TaskStatus.being_done,
                user_id=veroonika.id,
                assignee_id=jaanus.id,
            ),
            Task(
                title="PUSH TO GITHUB",
                description="Push the current changes to the master branch of the GitHub repository",
                status=TaskStatus.being_done,
                user_id=jaanus.id,
                assignee_id=None,
            ),
            Task(
                title="Clean the house",
                description="Vacuum the dust and mop the floors.",
                status=TaskStatus.todo,
                user_id=joonas.id,
                assignee_id=joonas.id,
            ),
            Task(
                title="Mentally prepare for friday conversation",
                description="Think about what I want to say and how to say it.",
                status=TaskStatus.being_done,
                user_id=veroonika.id,
                assignee_id=None,
            ),
        ]

        for task in tasks:
            db.add(task)   
        db.commit()
        for task in tasks:
            db.refresh(task) 

        print(f"Created {len(tasks)} tasks.")

        # Create comments
        comments = [
            Comment(
                content="I will start working on this task tomorrow.",
                task_id=tasks[0].id,
                user_id=joonas.id,
            ),
            Comment(
                content="I have some ideas on how to fix this issue.",
                task_id=tasks[0].id,
                user_id=veroonika.id,
            ),
            Comment(
                content="I will review the code and give feedback.",
                task_id=tasks[0].id,
                user_id=jaanus.id,
            ),
            Comment(
                content="I have updated the README file with the latest changes.",
                task_id=tasks[1].id,
                user_id=veroonika.id,
            ),
        ]

        for comment in comments:
            db.add(comment)
        db.commit()

        print(f"Created {len(comments)} comments.")
        print("Database seeding completed successfully.")
        print("\nTest Account Credentials:")
        print("Username: joonas, Password: password123")
        print("Username: veroonika, Password: password123")
        print("Username: jaanus, Password: password123")

    finally:
        db.close()

if __name__ == "__main__":
    seed()