from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Restaurant, Menu, Employee, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'created_at')
        read_only_fields = ('id', 'created_at')


class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        write_only=True,
        source='restaurant'
    )

    class Meta:
        model = Menu
        fields = ('id', 'restaurant', 'restaurant_id', 'date', 'dishes', 'created_at')
        read_only_fields = ('id', 'created_at')


class CreateMenuSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        write_only=True,
        source='restaurant'  # зв'язує поле restaurant_id з полем restaurant у моделі
    )

    class Meta:
        model = Menu
        fields = ('restaurant_id', 'date', 'dishes')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        read_only_fields = ('id',)


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ('id', 'user', 'phone')
        read_only_fields = ('id',)


class VoteSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        write_only=True,
        source='employee'
    )
    menu = MenuSerializer(read_only=True)
    menu_id = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all(),
        write_only=True,
        source='menu'
    )

    class Meta:
        model = Vote
        fields = ('id', 'employee', 'employee_id', 'menu', 'menu_id', 'created_at')
        read_only_fields = ('id', 'created_at')
