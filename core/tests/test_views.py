import pytest
from core.models import Menu, Vote
from datetime import date


@pytest.mark.django_db
def test_create_menu(api_client_with_token, restaurant):
    data = {
        "restaurant_id": restaurant.id,
        "date": str(date.today()),
        "dishes": ["Salad", "Soup", "Steak"],
    }
    response = api_client_with_token.post("/api/menus/", data, format="json")
    assert response.status_code == 201, f"Response data: {response.data}"
    assert Menu.objects.count() == 1
    menu = Menu.objects.first()
    assert menu.dishes == data["dishes"]


@pytest.mark.django_db
def test_today_menu(api_client_with_token, menu):
    response = api_client_with_token.get("/api/menus/today/")
    assert response.status_code == 200, f"Response data: {response.data}"
    assert len(response.data) >= 1
    assert response.data[0]["dishes"] == menu.dishes


@pytest.mark.django_db
def test_vote_menu_success(api_client_with_token, employee, menu):
    response = api_client_with_token.post(f"/api/menus/{menu.id}/vote/")
    assert response.status_code == 201
    assert Vote.objects.filter(employee=employee, menu=menu).exists()


@pytest.mark.django_db
def test_vote_menu_only_today(api_client_with_token, employee, restaurant):
    old_menu = Menu.objects.create(
        restaurant=restaurant,
        date=date(2020, 1, 1),
        dishes=["Old Dish"],
    )
    response = api_client_with_token.post(f"/api/menus/{old_menu.id}/vote/")
    assert response.status_code == 400
    assert response.data["detail"] == "can vote only for today menu"


@pytest.mark.django_db
def test_results_today(api_client_with_token, employee, menu):
    api_client_with_token.post(f"/api/menus/{menu.id}/vote/")

    response = api_client_with_token.get("/api/results/today/")
    assert response.status_code == 200
    assert response.data[0]["votes"] == 1
    assert response.data[0]["menu_id"] == menu.id
    assert response.data[0]["restaurant"] == menu.restaurant.name
