from . import views
from django.urls import path


urlpatterns = [
    path('', views.signUp, name='signUp'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
]
