from django.urls import path
from . import views

app_name = "rsh"

urlpatterns = [
    path("", views.panel, name="panel"),
    path("api/consulta/", views.api_rsh, name="api_rsh"),
]