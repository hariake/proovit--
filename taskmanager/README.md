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
4. Run the backend
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
6. Open the app
go to http://localhost:5173 in your browser (default vite port, if you have other apps running vite will give you the next port. See the terminal)

7. Register an account and start creating tasks

## Stop the app
```bash
docker compse down
```

## Wipe the database
```bash
docker compose down -v
```