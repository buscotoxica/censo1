from django.urls import path
from django.views.generic import TemplateView

app_name = 'logging'

urlpatterns = [
    path('', TemplateView.as_view(template_name='logging/panel.html'), name='panel'),
]