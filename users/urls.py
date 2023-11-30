from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('status', views.status, name='status'),
    path('welcome', views.welcome, name='index'),
    path('register', views.register),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('password', views.password, name='password'),

]
