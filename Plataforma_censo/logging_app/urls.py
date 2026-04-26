from django.urls import path
from django.views.generic import TemplateView
from .views import verificar_email,enviar_comprobante,estado_email
from . import views 

app_name = 'logging'

urlpatterns = [
    path('', TemplateView.as_view(template_name='logging/panel.html'), name='panel'),
    path("registrar-click/", views.registrar_click, name="registrar_click"),
    path('verificar-email/', verificar_email, name='verificar_email'),
    path('enviar-comprobante/', enviar_comprobante, name='enviar_comprobante'),
    path('estado-email/', estado_email, name='estado_email'),
]
