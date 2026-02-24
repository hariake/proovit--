# Task Manager

A Lightweight taskmanager built with Python/Tornado, PostgreSQL and React

## Features

 +++ User Registration and login +++
 +++ Create, edit and delete tasks with multiple forms of data +++
 +++ Drag and drop task dashboard +++
 +++ Filter tasks by: My tasks, All tasks, Done tasks +++
 +++ Comment on tasks +++

 ## Tech Stack

 **Backend:** Python, Tornado, SQLAlchemy, PostgreSQL, Alembic
 **Frontend:** React, TypeScript, Vite, Tailwind CSS
 **infra:** Docker, Docker Compose, Nginx

 ## Requirements

 +++ Docker +++
 +++ Docker compose +++

 ## How to run the app

 1. Clone the repo
```bash
   git clone https://github.com/hariake/proovit--.git
   cd proovit--/taskmanager
```
2. Create a `.env` file based on `.env.example`
```bash
   cp .env.example .env
```
3. Start the app
```bash
   docker compose up --build
```
4. Open http://localhost in your browser

5. Register an account and start creating tasks

## Stop the app
```bash
docker compse down
```

## Wipe the database
```bash
docker compose down -v
```