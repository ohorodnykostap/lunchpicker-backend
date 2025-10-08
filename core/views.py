from datetime import date

from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Restaurant, Menu, Employee, Vote
from .serializers import (
    RestaurantSerializer,
    MenuSerializer,
    CreateMenuSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CreateMenuSerializer
        return MenuSerializer

    @action(detail=False, methods=['get'], url_path='today')
    def today(self, request):
        today_date = date.today()
        menus = Menu.objects.filter(date=today_date).select_related('restaurant')
        serializer = MenuSerializer(menus, many=True)

        # Підтримка старих клієнтів
        build_version = getattr(request, 'build_version', None)
        if build_version and build_version.startswith('1.'):
            data = [
                {'restaurant': m['restaurant']['name'], 'dishes': m['dishes']}
                for m in serializer.data
            ]
            return Response(data)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_employee(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    phone = request.data.get('phone', '')

    if not username or not password:
        return Response(
            {'detail': 'username and password required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'detail': 'username exists'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(username=username, password=password, email=email)
    emp = Employee.objects.create(user=user, phone=phone)
    return Response({'id': emp.id, 'username': user.username},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_menu(request, menu_id):
    user = request.user
    try:
        emp = user.employee
    except Employee.DoesNotExist:
        return Response(
            {'detail': 'employee profile not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        menu = Menu.objects.get(id=menu_id)
    except Menu.DoesNotExist:
        return Response(
            {'detail': 'menu not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if menu.date != date.today():
        return Response(
            {'detail': 'can vote only for today menu'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    vote, created = Vote.objects.get_or_create(employee=emp, menu=menu)
    if not created:
        return Response(
            {'detail': 'already voted for this menu'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response({'detail': 'voted'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def results_today(request):

    today_date = date.today()
    menus = (
        Menu.objects.filter(date=today_date)
        .select_related('restaurant')
        .prefetch_related('votes')
    )
    results = [
        {
            'menu_id': menu.id,
            'restaurant': menu.restaurant.name,
            'votes': menu.votes.count(),
            'dishes': menu.dishes,
        }
        for menu in menus
    ]
    results.sort(key=lambda x: x['votes'], reverse=True)
    return Response(results)
