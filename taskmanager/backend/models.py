from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timezone
import enum

Base = declarative_base()

# TaskStatus enum that defines the possible status values for a task.
class TaskStatus(enum.Enum):
    todo = "todo"
    being_done = "being_done"
    done = "done"

# Models that give SQLAlchemy the structure of the database tables and how they relate to each other. 
    
class User(Base):
    __tablename__ = 'users'
     
    id = Column(Integer, primary_key=True) #primary key that uniquely identifies each user in the database
    username = Column(String(25), unique=True, nullable=False) #username field that must be unique and cannot be null
    password_hash = Column(String(255), nullable=False) #password hash field that stores the hashed password, cannot be null
    created_at = Column(DateTime(timezone=True), server_default=func.now()) #timestamp of when the user was created, defaults to the current time
    
    tasks = relationship('Task', back_populates='user', foreign_keys='Task.user_id') #relationship that allows us to access the tasks created by the user through user.tasks, foreign key is Task.user_id


class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True) #primary key that uniquely identifies each task in the database
    title = Column(String(100), nullable=False) #title field that cannot be null
    description = Column(String(1500)) #description field that can be null
    status = Column(Enum(TaskStatus, name="task_status"), default=TaskStatus.todo) #status field that uses the TaskStatus enum, defaults to "todo"
    created_at = Column(DateTime(timezone=True), server_default=func.now()) #timestamp of when the task was created, defaults to the current time
    updated_at = Column(DateTime(timezone=True), server_default=func.now()) #timestamp of when the task was last updated, defaults to the current time
    deadline = Column(DateTime(timezone=True), nullable=True) #deadline field that can be null, stores the deadline of the task as a datetime object with timezone information

    user_id = Column(Integer, ForeignKey('users.id')) #foreign key that links the task to the user who created it.
    assignee_id = Column(Integer, ForeignKey('users.id'), nullable=True) #foreign key that links the task to the user who is assigned to do it.
    
    user = relationship('User', back_populates='tasks', foreign_keys=[user_id]) #relationship that allows us to access the user who created the task through task.user
    assignee = relationship('User', foreign_keys=[assignee_id]) #relationship that allows us to access the user who is assigned to do the task through task.assignee
    comments = relationship('Comment', back_populates='task', cascade="all, delete-orphan") #relationship that allows us to access the comments that belong to the task through task.comments, if a task is deleted, its comments will also be deleted
    
class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True) #primary key that uniquely identifies each comment in the database
    content = Column(String(1500), nullable=False) #content field that cannot be null, stores the content of the comment
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False) #foreign key that links the comment to the task it belongs to
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) #foreign key that links the comment to the user who made it
    created_at = Column(DateTime(timezone=True), server_default=func.now()) #timestamp of when the comment was created, defaults to the current time

    task = relationship('Task', back_populates='comments') #relationship that allows us to access the task that the comment belongs to through comment.task
    user = relationship('User') #relationship that allows us to access the user who made the comment through comment.user