from . import views
from django.urls import path


urlpatterns = [
    path('', views.signUp, name='signUp'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('varifying/', views.varifying, name='varifying'),
    path('password_forget/', views.password_forget, name='password_forget'),
    path('password_reset/>', views.password_reset, name='password_reset'),
]
