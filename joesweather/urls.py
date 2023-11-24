from django.urls import path
from . import views


urlpatterns = [
    path("", views.temperature_forecast, name="home"),
]
