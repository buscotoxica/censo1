from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Omz, Sb, Uv, Censo, CensoUv, RegistroConsulta
from .serializers import OmzSerializer, SbSerializer, UvSerializer, CensoSerializer, CensoUvSerializer
import json
from logging_app.models import RegistroAcceso

# ---------- VISTA HTML DEL PANEL ----------
from django.http import JsonResponse
from .omz import POLIGONOS_OMZ, ETIQUETAS_OMZ

from django.http import JsonResponse
from .uv import POLIGONOS_UV, ETIQUETAS_UV
 
from django.http import JsonResponse
from .sb import POLIGONOS_BARRIOS, ETIQUETAS_BARRIOS
 
 
def sb_geojson(request):
    """
    GET /censo/api/sb-geojson/
 
    Devuelve los polÃ­gonos de todos los Sectores Barriales.
    Formato:
    {
        "barrioEjemplo": { "etiqueta": "Barrio Laguna Verde", "coords": [[-33.10, -71.67], ...] },
        ...
    }
    """
    resultado = {}
    for clave, coordenadas in POLIGONOS_BARRIOS.items():
        etiqueta = ETIQUETAS_BARRIOS.get(clave, clave)
        resultado[clave] = {
            "etiqueta": etiqueta,
            "coords": [[lat, lng] for lat, lng in coordenadas]
        }
    return JsonResponse(resultado)
 
def uv_geojson(request):
    """
    GET /censo/api/uv-geojson/
 
    Devuelve los polÃ­gonos de todas las UV disponibles.
    Formato:
    {
        "uv1": { "etiqueta": "UV 1", "coords": [[-33.03, -71.58], ...] },
        "uv2": { "etiqueta": "UV 2", "coords": [...] },
        ...
    }
    """
    resultado = {}
    for clave, coordenadas in POLIGONOS_UV.items():
        etiqueta = ETIQUETAS_UV.get(clave, clave)
        resultado[clave] = {
            "etiqueta": etiqueta,
            # Tuplas (lat, lng) ? [lat, lng] para Leaflet
            # El HTML invertirÃ¡ a [lng, lat] para Mapbox
            "coords": [[lat, lng] for lat, lng in coordenadas]
        }
    return JsonResponse(resultado)
 
def omz_geojson(request):
    """
    GET /censo/api/omz-geojson/

    Devuelve un JSON con los polÃ­gonos de todas las OMZ disponibles.
    Formato:
    {
        "omzNueva":      { "etiqueta": "OMZ Baron",      "coords": [[-33.03, -71.59], ...] },
        "omzEsperanza":  { "etiqueta": "OMZ Esperanza",  "coords": [[-33.02, -71.58], ...] },
        ...
    }
    """
    resultado = {}

    for clave, coordenadas in POLIGONOS_OMZ.items():
        etiqueta = ETIQUETAS_OMZ.get(clave, clave)   # fallback a la clave si no hay etiqueta
        resultado[clave] = {
            "etiqueta": etiqueta,
            # Las tuplas (lat, lng) de Python se convierten a [lat, lng] para Leaflet
            "coords": [[lat, lng] for lat, lng in coordenadas],
        }

    return JsonResponse(resultado)

def panel_censo(request):
    """
    Panel principal para Censo: solo carga el HTML.
    Los filtros se llenan por AJAX contra las APIs de abajo.
    """
    return render(request, 'censo/panel.html')


# ---------- APIs para combos ----------

@api_view(['GET'])
def api_omz_list(request):
    qs = Omz.objects.all().order_by('nombre')
    data = OmzSerializer(qs, many=True).data
    return Response(data)


@api_view(['GET'])
def api_sb_list(request):
    omz_id = request.GET.get('omz')
    qs = Sb.objects.all()
    if omz_id:
        qs = qs.filter(id_omz_id=omz_id)
    qs = qs.order_by('nombre')
    data = SbSerializer(qs, many=True).data
    return Response(data)


@api_view(['GET'])
def api_uv_list(request):
    omz_id = request.GET.get('omz')
    sb_id = request.GET.get('sb')

    qs = Uv.objects.select_related('id_sb', 'id_sb__id_omz')

    if sb_id:
        qs = qs.filter(id_sb_id=sb_id)
    if omz_id:
        qs = qs.filter(id_sb__id_omz_id=omz_id)

    qs = qs.order_by('cod_uv')
    data = UvSerializer(qs, many=True).data
    return Response(data)


@api_view(['GET'])
def api_censo_annios(request):
    qs = Censo.objects.all().order_by('annio')
    data = CensoSerializer(qs, many=True).data
    return Response(data)


# ---------- API principal de consulta ----------
from django.db import transaction
@api_view(['POST'])
def api_censo_consulta(request):

    print("USER:", request.user)
    print("AUTH:", request.user.is_authenticated)
    print("ENTRÃ A api_censo_consulta")

    payload = request.data
    print("PAYLOAD RECIBIDO:", payload)

    uv_list = payload.get('uv') or []
    sb_list = payload.get('sb') or []
    omz_list = payload.get('omz') or []
    annio_list = payload.get('annios') or []

    # ? Obtener email de forma segura
    email = request.user.email if request.user.is_authenticated else payload.get('email')

    print("EMAIL USADO:", email)

    # ? Registrar acceso solo si hay email
    if email:
        try:
            with transaction.atomic():
                RegistroAcceso.objects.create(
                    email=email,
                    panel="CENSO",
                    tipo="consulta",
                    parametros={
                        "uv": uv_list,
                        "sb": sb_list,
                        "omz": omz_list,
                        "annios": annio_list,
                        "metricas": payload.get("metricas"),
                    }
                )
        except Exception as e:
            print("ERROR LOG CENSO:", e)

    # ?? Queryset
    qs = CensoUv.objects.select_related(
        'id_censo',
        'id_uv',
        'id_uv__id_sb',
        'id_uv__id_sb__id_omz'
    )

    if uv_list:
        qs = qs.filter(id_uv__cod_uv__in=uv_list)

    if sb_list:
        qs = qs.filter(id_uv__id_sb_id__in=sb_list)

    if omz_list:
        qs = qs.filter(id_uv__id_sb__id_omz_id__in=omz_list)

    if annio_list:
        qs = qs.filter(id_censo__annio__in=annio_list)

    serializer = CensoUvSerializer(qs, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

def panel_censo_uv(request):
    # Todas las UV
    uvs = Uv.objects.all().order_by("cod_uv")

    # AÃ±os disponibles
    anios = Censo.objects.values_list("annio", flat=True).order_by("annio")

    # Filtros disponibles (igual que tu Java)
    filtros = [
        ("area", "Ãrea"),
        ("total_pers", "Total de Personas"),
        ("densidad", "Densidad"),
        ("total_vivi", "Total de Viviendas"),
        ("hombres", "Hombres"),
        ("mujeres", "Mujeres"),
        ("edad_0a5", "Edad 0-5 aÃ±os"),
        ("edad_6a14", "Edad 6-14 aÃ±os"),
        ("edad_15a64", "Edad 15-64 aÃ±os"),
        ("edad_64ymas", "Edad 65+ aÃ±os"),
        ("iam", "IAM"),
        ("idd", "IDD"),
    ]

    return render(request, "censo/panel_uv.html", {
        "uvs": uvs,
        "anios": anios,
        "filtros": filtros
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

@api_view(["POST"])
def censo_uv_query(request):
    print("ENTRÃ A censo_uv_query")
    fields = request.data.get("fields", [])
    filterValues = request.data.get("filterValues", [])
    annio = request.data.get("annio")
    filterType = request.data.get("filterType")

    # ConstrucciÃ³n del SQL DINÃMICO
    columnas = ", ".join(fields)

    sql = f"""
        SELECT uv.cod_uv, {columnas}
        FROM censo_uv cuv
        JOIN uv ON uv.cod_uv = cuv.id_uv
        WHERE cuv.id_censo = %s AND cuv.id_uv = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [annio, filterValues[0]])
        rows = cursor.fetchall()

    resultado = []
    for row in rows:
        item = {"codUv": row[0]}
        for i, f in enumerate(fields):
            item[f] = row[i+1]
        resultado.append(item)

    return Response(resultado)

