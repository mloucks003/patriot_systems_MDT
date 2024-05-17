from django.urls import path
from .views import plate_check

urlpatterns = [
    path('plate_check/', plate_check, name='plate_check'),
]
