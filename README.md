# Price Tracker

A Django-based web application that tracks product prices from various e-commerce platforms and notifies users when prices drop.

## Features

- Track product prices from multiple e-commerce platforms (currently supports Flipkart)
- User authentication and authorization using JWT
- Email notifications for price drops
- RESTful API endpoints
- Asynchronous task processing with Celery
- Redis for task queue management

## Tech Stack

- Python 3.x
- Django 4.2
- Django REST Framework
- Celery
- Redis
- SQLite (Development)
- JWT Authentication

## Prerequisites

- Python 3.x
- Redis Server
- Virtual Environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PriceTracker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Create a `.env` file in the project root
- Add the following variables:
  ```
  SECRET_KEY=your_secret_key
  EMAIL_HOST_USER=your_email@gmail.com
  EMAIL_HOST_PASSWORD=your_app_password
  ```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start Redis server:
```bash
redis-server
```

7. Start Celery worker:
```bash
celery -A PriceTracker worker -l info
```

8. Start Celery beat:
```bash
celery -A PriceTracker beat -l info
```

9. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
PriceTracker/
├── account/             # User authentication and management
├── product/            # Product tracking functionality
│   ├── crawler.py      # Web crawler for e-commerce sites
│   ├── models.py       # Database models
│   └── tasks.py        # Celery tasks
├── PriceTracker/       # Project configuration
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies
```

## API Endpoints

- `/api/auth/` - Authentication endpoints
- `/api/products/` - Product tracking endpoints
- `/api/tracking/` - Price tracking management endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or support, please contact:
- Email: rajendra95.work@gmail.com 
