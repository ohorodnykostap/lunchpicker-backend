from datetime import date

import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

from core.models import Employee, Restaurant, Menu, Vote


@pytest.mark.django_db
def test_employee_str():
    user = User.objects.create(username="john")
    emp = Employee.objects.create(user=user, phone="12345")
    assert str(emp) == "john"


@pytest.mark.django_db
def test_restaurant_str_and_unique_name():
    r = Restaurant.objects.create(name="Pizzeria")
    assert str(r) == "Pizzeria"

    with pytest.raises(IntegrityError):
        Restaurant.objects.create(name="Pizzeria")


@pytest.mark.django_db
def test_menu_str_and_unique_together(restaurant):
    menu = Menu.objects.create(
        restaurant=restaurant, date=date.today(), dishes=["Soup"]
    )
    assert str(menu) == f"{restaurant.name} - {date.today()}"

    with pytest.raises(IntegrityError):
        Menu.objects.create(
            restaurant=restaurant, date=date.today(), dishes=["Pizza"]
        )


@pytest.mark.django_db
def test_vote_unique_together(employee, menu):
    vote = Vote.objects.create(employee=employee, menu=menu)
    assert str(vote) == f"{employee.user.username} voted for {menu}"

    with pytest.raises(IntegrityError):
        Vote.objects.create(employee=employee, menu=menu)
