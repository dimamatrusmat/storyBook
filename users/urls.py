from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.account_register, name='register'),
]
