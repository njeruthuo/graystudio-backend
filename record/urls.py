from django.urls import path
from . import views

urlpatterns = [
    path('client_api_view/', views.client_api_view, name='client_api_view'),
]
