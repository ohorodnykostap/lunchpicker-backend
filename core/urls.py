from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RestaurantViewSet,
    MenuViewSet,
    create_employee,
    vote_menu,
    results_today,
)


router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'menus', MenuViewSet, basename='menu')

urlpatterns = [

    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('', include(router.urls)),

    path('employees/create/', create_employee, name='create_employee'),
    path('menus/<int:menu_id>/vote/', vote_menu, name='vote_menu'),
    path('results/today/', results_today, name='results_today'),
]
