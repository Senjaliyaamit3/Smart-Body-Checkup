from django.urls import path
from . import views

urlpatterns = [
    path("",                      views.prediction,     name="prediction"),
    path("report/<int:pk>/",      views.download_report, name="download_report"),
]