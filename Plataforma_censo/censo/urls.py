from django.urls import path
from . import views

app_name = 'censo'

urlpatterns = [
    path('', views.panel_censo, name='panel'),

    # APIs
    path('api/omz/', views.api_omz_list, name='api_omz'),
    path('api/sb/', views.api_sb_list, name='api_sb'),
    path('api/uv/', views.api_uv_list, name='api_uv'),
    path('api/censos/', views.api_censo_annios, name='api_censos'),
    path('api/consulta/', views.api_censo_consulta, name='api_consulta'),
    path("api/omz-geojson/", views.omz_geojson, name="omz-geojson"),
    path("api/uv-geojson/", views.uv_geojson, name="uv-geojson"),
    path("api/sb-geojson/", views.sb_geojson, name="sb-geojson"),
    

]