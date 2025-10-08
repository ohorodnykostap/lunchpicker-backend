# LunchPicker Backend

This is the backend service for the LunchPicker project, built with Django and Docker.

## Prerequisites

- Docker
- Docker Compose
- Python 3.10+ (if running outside Docker)

## Setup and Run

1. **Clone the repository:**

bash
git clone <your-repo-url>
cd lunchpicker/backend

1.Build and start Docker containers:
docker-compose up --build -d

2.Build and start Docker containers:
docker-compose up --build -d

3.Apply database migrations:
docker-compose exec web python manage.py migrate

4.Create a superuser (optional):
docker-compose exec web python manage.py createsuperuser

Running Tests and Code Style Check

1.Run Django tests with pytest:
docker-compose exec web pytest

2.Check Python code style with flake8:
docker-compose exec web flake8 .

## API Endpoints

### Authentication
- `POST /auth/token/` — obtain JWT token (login)
- `POST /auth/token/refresh/` — refresh JWT token

### Restaurants
- `GET /restaurants/` — list all restaurants
- `POST /restaurants/` — create a restaurant 
- `GET /restaurants/{id}/` — retrieve restaurant details
- `PUT /PATCH /restaurants/{id}/` — update restaurant

### Menus
- `GET /menus/` — list all menus
- `POST /menus/` — create a menu
- `GET /menus/{id}/` — retrieve menu details
- `PUT /PATCH /menus/{id}/` — update menu
- `DELETE /menus/{id}/` — delete menu

### Custom Endpoints
- `POST /menus/{menu_id}/vote/` — vote for a menu
- `GET /results/today/` — get today's voting results
- `POST /employees/create/` — create a new employee
