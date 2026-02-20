import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://postgres:password@localhost:5432/taskmanager"
)

engine =create_engine(
    DATABASE_URL,
    pool_size=5, #holds open 5 connections to the database at alltime
    max_overflow=10, #if the 5 conenctions are all in use while more are needed opens up to 10 more connections
    pool_pre_ping=True #tests the connections before using them
)

SessionLocal = scoped_session(sessionmaker(bind=engine)) #opens a db sessions for each request and after db work is done commits the sessiond and closes it.