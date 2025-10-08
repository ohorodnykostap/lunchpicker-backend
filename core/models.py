from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='employee'
    )
    phone = models.CharField(max_length=30, blank=True)
    app_version = models.CharField(max_length=20, default='1.0')

    def __str__(self):
        return self.user.username


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='menus'
    )
    date = models.DateField()
    dishes = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('restaurant', 'date')

    def __str__(self):
        return f'{self.restaurant.name} - {self.date}'


class Vote(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='votes'
    )
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='votes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'menu')

    def __str__(self):
        return f'{self.employee.user.username} voted for {self.menu}'
