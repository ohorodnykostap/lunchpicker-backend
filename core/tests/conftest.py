import uuid
from datetime import date

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Employee, Restaurant, Menu


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    unique_username = f"testuser_{uuid.uuid4().hex[:6]}"
    return User.objects.create_user(username=unique_username, password="password123")


@pytest.fixture
def employee(db, user):
    return Employee.objects.create(user=user, phone="+380961234567")


@pytest.fixture
def restaurant(db):
    return Restaurant.objects.create(
        name=f"Restaurant_{uuid.uuid4().hex[:6]}", address="123 Main St"
    )


@pytest.fixture
def menu(db, restaurant):
    return Menu.objects.create(
        restaurant=restaurant,
        date=date.today(),
        dishes=["Salad", "Soup", "Steak"],
    )


@pytest.fixture
def api_client_with_token(db, user, employee):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client
