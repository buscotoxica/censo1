from django.urls import path
from django.views.generic import TemplateView

from . import views 

app_name = 'logging'

urlpatterns = [
    path('', TemplateView.as_view(template_name='logging/panel.html'), name='panel'),
    path("registrar-click/", views.registrar_click, name="registrar_click"),
]
