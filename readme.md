# 📝 Todo List API

A simple task management API built with **Django** and **Django REST Framework**, featuring:

- ✅ JWT authentication (access and refresh tokens)
- ✅ HttpOnly refresh token cookies
- ✅ Token blacklisting (logout and refresh)
- ✅ Custom Django middleware for token extraction
- ✅ PostgreSQL as the database
- ✅ Full CRUD for tasks, scoped to authenticated users
- ✅ Fully tested with Django’s test framework

---

## 🛠 Tech Stack

- **Framework**: Django, Django REST Framework
- **Auth**: SimpleJWT
- **Database**: PostgreSQL
- **Testing**: Django TestCase

---

## 📁 Project Structure

```
todo-list-api/
├── auth_service/       
├── tasks/           
├── todo_list_api/      
├── manage.py
└── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/M-Elhawawshy/todo-api.git
cd todo-list-api
```

### 2. Create a virtual environment and activate it

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create the database and user, Example:
```sql
CREATE DATABASE todo;
CREATE USER todo_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE todo TO todo_user;
```

Update `settings.py` with:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<name>',
        'USER': '<user_name>',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the server

```bash
python manage.py runserver
```

---

## 🔐 Authentication Flow

- **Login**: returns access and refresh tokens. Refresh token is stored in an HttpOnly cookie.
- **Refresh**: uses refresh token from cookie to issue new tokens.
- **Logout**: blacklists the refresh token.
- Middleware extracts and validates the access token for authenticated endpoints.

---

## ✅ Task API Endpoints

All routes under `/api/tasks` require a valid access token.

| Method | Endpoint                   | Description       |
|--------|----------------------------|-------------------|
| POST   | `/api/auth_service/signup` | user signup       |
| POST   | `/api/auth_service/login`  | user login        |
| POST   | `/api/auth_service/logout` | user logout       |
| POST   | `/api/tasks/`              | Create a task     |
| GET    | `/api/tasks/`              | List user's tasks |
| GET    | `/api/tasks/<id>/`         | Get task by ID    |
| PATCH  | `/api/tasks/<id>/`         | Update a task     |
| DELETE | `/api/tasks/<id>/`         | Delete a task     |

---

## 🧪 Running Tests

Tests are isolated and run using a temporary test database.

```bash
python manage.py test auth_service.tests tasks.tests
```

Test coverage includes:

- Auth service: signup, login, refresh, logout
- Task service: create, retrieve, update, delete

---

## 🧠 Additional Features

- Custom user model (`TasksUser`) using UUID as primary key
- Passwords are hashed securely
- Blacklisted refresh tokens stored and checked via `token_blacklist`
- Custom middleware attaches `user_id` to `request` based on access token
- Clean architecture with modular app design

---

