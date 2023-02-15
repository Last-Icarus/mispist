from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name="home"),
    
    path('create_team/', views.createTeam, name="create-team"),
    path('team/<str:pk>/', views.team, name="team"),

    
] 
