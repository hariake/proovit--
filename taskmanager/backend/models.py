from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timezone
import enum

Base = declarative_base()

class TaskStatus(enum.Enum):
    todo = "todo"
    being_done = "being_done"
    done = "done"
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    tasks = relationship('Task', back_populates='user') 
class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1500))
    status = Column(Enum(TaskStatus, name="task_status"), default=TaskStatus.todo)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    deadline = Column(DateTime(timezone=True), nullable=True)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='tasks')
