from django.urls import path
from . import views

app_name    = 'fitness'
urlpatterns = [
    path('', views.Home, name="home"),
    path('fitness_category/', views.fitness_category, name="fitness_category"),
    path('fitness_memory/', views.fitness_memory, name="fitness_memory"),

    path('food_category/', views.food_category, name="food_category"),
    path('food_memory/', views.food_memory, name="food_memory"),

    path('menu/', views.menu, name="menu"),
    path('menu/<uuid:pk>/', views.menu, name="menu_single"),


    path('target/', views.target, name="target"),
    path('target/<uuid:pk>/', views.target, name="target_single"),
]
