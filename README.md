# TaskManager
An app to prioritize and plan your daily tasks to de-clutter your mind and maintain a stress-free routine

## File Structure
With the help of Claude, the following file structure will be followed for v1:

task-manager-api/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app (entry point)
│   │   ├── STRUCTURE.md
│   │   │
│   │   ├── core/                      # 🎯 Core (spend most time here)
│   │   │   ├── __init__.py
│   │   │   ├── config.py              # Settings with pydantic-settings
│   │   │   ├── models.py              # SQLAlchemy models
│   │   │   ├── schemas.py             # Pydantic schemas
│   │   │   ├── dependencies.py        # Dependency injection
│   │   │   ├── database.py            # DB connection & session
│   │   │   ├── security.py            # JWT, password hashing
│   │   │   └── exceptions.py          # Custom exceptions
│   │   │
│   │   ├── api/                       # 🚀 API endpoints (main focus)
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── endpoints/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── tasks.py       # Task CRUD + advanced queries
│   │   │       │   ├── auth.py        # Login, register, refresh token
│   │   │       │   ├── users.py       # User management
│   │   │       │   └── stats.py       # Analytics & reporting
│   │   │       └── api.py             # Router aggregation
│   │   │
│   │   ├── services/                  # 🔧 Business logic (key learning)
│   │   │   ├── __init__.py
│   │   │   ├── task_service.py        # Complex task operations
│   │   │   ├── user_service.py        # User operations
│   │   │   ├── cache_service.py       # Redis caching patterns
│   │   │   ├── notification_service.py # Background notifications
│   │   │   └── analytics_service.py   # Data aggregation
│   │   │
│   │   ├── tasks/                     # 📋 Background tasks (Celery/APScheduler)
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py          # Celery configuration
│   │   │   ├── scheduled_tasks.py     # Cron jobs
│   │   │   └── task_reminders.py      # Email/notification tasks
│   │   │
│   │   ├── middleware/                # 🛡️ Middleware (important!)
│   │   │   ├── __init__.py
│   │   │   ├── auth_middleware.py     # JWT validation
│   │   │   ├── rate_limit.py          # Rate limiting
│   │   │   ├── logging.py             # Request/response logging
│   │   │   └── error_handler.py       # Global error handling
│   │   │
│   │   ├── utils/                     # 🔨 Utilities
│   │   │   ├── __init__.py
│   │   │   ├── pagination.py          # Pagination helpers
│   │   │   ├── validators.py          # Custom validators
│   │   │   └── datetime_utils.py      # Date/time helpers
│   │   │
│   │   ├── tests/                     # 🧪 Testing (crucial for backend)
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py            # Pytest fixtures
│   │   │   ├── test_tasks.py
│   │   │   ├── test_auth.py
│   │   │   ├── test_services.py
│   │   │   └── test_integration.py
│   │   │
│   │   ├── web/                       # 🌐 Simple frontend (minimal)
│   │   │   ├── __init__.py
│   │   │   └── routes.py              # Jinja2 template routes
│   │   │
│   │   ├── static/                    # Static files (very simple)
│   │   │   ├── css/
│   │   │   │   └── style.css          # Minimal CSS
│   │   │   └── js/
│   │   │       └── app.js             # Vanilla JS for API calls
│   │   │
│   │   └── templates/                 # Jinja2 templates (simple)
│   │       ├── base.html
│   │       ├── index.html             # Main page (just shows tasks)
│   │       └── docs.html              # API documentation page
│   │
│   ├── alembic/                       # 📝 Database migrations (important!)
│   │   ├── versions/
│   │   │   ├── 001_initial.py
│   │   │   ├── 002_add_users.py
│   │   │   └── 003_add_categories.py
│   │   ├── env.py
│   │   └── alembic.ini
│   │
│   ├── scripts/                       # 🛠️ Utility scripts
│   │   ├── seed_data.py               # Populate test data
│   │   ├── reset_db.py                # Reset database
│   │   └── create_admin.py            # Create admin user
│   │
│   ├── requirements.txt
│   ├── requirements-dev.txt           # Dev dependencies
│   ├── Dockerfile
│   ├── .env.example
│   └── pytest.ini
│
├── docker-compose.yml
├── docker-compose.dev.yml             # Development override
├── Makefile                           # Common commands
└── README.md
