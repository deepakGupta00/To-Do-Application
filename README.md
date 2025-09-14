# To-Do List Web Application  

A **Django-based To-Do List Application** that demonstrates:  
- REST API development (CRUD operations)  
- Raw SQL database integration (**no ORM used**)  
- HTML template rendering for UI  
- Automated testing with **pytest**  
- Clean, maintainable code with proper logging & exception handling  

## Features  

- **Create Tasks** — add title, description, and due date  
- **View Tasks** — see all tasks sorted by creation date  
- **Update Tasks** — mark tasks as completed  
- **Delete Tasks** — remove tasks from the list  
- **REST APIs** — easily integrate with external systems  
- **Automated Tests** — pytest coverage for all endpoints

## Project Structure

```
todo_project/
├── tasks/               # Task management app
├── todo_project/        # Project settings and URLs
├── db.sqlite3           # SQLite database
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker support
└── manage.py            # Django management script
```

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/deepakGupta00/TO-DO-Project.git
cd TO-DO-Project
```
### Create Virtual Environment

```sh
python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Run migrations

```sh
python manage.py migrate
```


### 5. Start the development server

```sh
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.

## Docker

To run with Docker:

```sh
docker build -t django-todo-app .
docker run -p 8000:8000 django-todo-app
```


### Running Tests
We use `pytest` for testing API endpoints.

```bash
pip install pytest pytest-django
pytest -v


### Folder Overview

- [`tasks/`](tasks/) - Contains task views, templates logic.
- [`tasks/templates/`](tasks/templates/) - HTML templates for tasks.
- [`todo_project/settings.py`](todo_project/settings.py) - Django settings.

---

**Made with Django & Bootstrap 5**