from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from censo.models import Sb   # <--- IMPORT CORRECTO
from .models import Datos
from censo.models import Omz

def panel(request):
    return render(request, "rsh/panel.html")


# o1: ¿Está trabajando?  (1=Sí, 2=No)
O1_KEY = {
    1: "trabaja_si",
    2: "trabaja_no",
}

# o2: Ocupación actual
O2_KEY = {
    1: "ocup_patron",
    2: "ocup_cuenta_propia",
    3: "ocup_empleado",
    4: "ocup_familiar_no_rem",
    5: "ocup_serv_domestico",
    6: "ocup_ffaa_orden",
}

# o3: Rama de actividad
O3_KEY = {
    1: "rama_agropecuaria",
    2: "rama_minera",
    3: "rama_industrial",
    4: "rama_energia",
    5: "rama_construccion",
    6: "rama_comercio_hoteles",
    7: "rama_transporte_com",
    8: "rama_financiera",
    9: "rama_servicios_sociales",
}

# o4: Tipo de ocupación
O4_KEY = {
    1: "ocup_permanente",
    2: "ocup_temporada",
    3: "ocup_ocasional",
    4: "ocup_prueba",
    5: "ocup_plazo_determinado",
}

# o5: ¿Tiene contrato? (1=Sí, 2=No)
O5_KEY = {
    1: "tiene_contrato_si",
    2: "tiene_contrato_no",
}

# o6: Tipo de contrato
O6_KEY = {
    1: "contrato_indefinido",
    2: "contrato_plazo_fijo",
    3: "contrato_obra_faena",
    4: "contrato_aprendizaje",
    5: "contrato_no_corresponde",
}

# o7: Horas semanales
O7_KEY = {
    1: "horas_menor_20",
    2: "horas_20_39",
    3: "horas_40_48",
    4: "horas_mayor_48",
}

# o8: ¿Buscó trabajo? (1=Sí, 2=No)
O8_KEY = {
    1: "busco_trabajo_si",
    2: "busco_trabajo_no",
}

# o9: Razón por la que no buscó trabajo
O9_KEY = {
    1: "no_busco_quehaceres_hogar",
    2: "no_busco_no_quien_ninos",
    3: "no_busco_enfermedad_cronica",
    4: "no_busco_cuida_enfermo",
    5: "no_busco_estudiante",
    6: "no_busco_jubilado",
    7: "no_busco_rentista",
    8: "no_busco_aburrido",
    9: "no_busco_no_interes",
    10: "no_busco_otra_razon",
}

SALUD_KEY = {
    "s1a": "salud_ceguera",
    "s1b": "salud_sordera",
    "s1c": "salud_mudez",
    "s1d": "salud_movilidad",
    "s1e": "salud_mental",
    "s1f": "salud_psiquiatrico",

    "s2a": "salud_salir_solo",
    "s2b": "salud_compras_solo",
    "s2c": "salud_bano_solo",
    "s2d": "salud_moverse_casa",
    "s2e": "salud_esfinter",
}

SALUD_LABEL = {
    "s1a": "Ceguera / dificultad visual",
    "s1b": "Sordera / dificultad auditiva",
    "s1c": "Mudez / dificultad en el habla",
    "s1d": "Dificultad física / movilidad",
    "s1e": "Problemas mentales",
    "s1f": "Problemas psiquiátricos",

    "s2a": "Puede salir solo(a)",
    "s2b": "Puede hacer compras solo(a)",
    "s2c": "Puede bañarse/comer solo(a)",
    "s2d": "Puede moverse dentro de la casa",
    "s2e": "Control de esfínteres",
}

PARENTESCO_KEY = {
    1: "jefe_hogar",
    2: "conyuge_pareja",
    3: "hijo_ambos",
    4: "hijo_solo_jefe",
    5: "hijo_solo_conyuge",
    6: "padre_madre",
    7: "suegro_suegra",
    8: "yerno_nuera",
    9: "nieto",
    10: "hermano",
    11: "cunado",
    12: "otro_familiar",
    13: "no_familiar",
}

INDIGENA_KEY = {
    0: "no_pertenece",
    1: "aimara",
    2: "rapa_nui",
    3: "quechua",
    4: "mapuche",
    5: "atacameno",
    6: "coyas",
    7: "kawesqar",
    8: "yagan",
    9: "diaguita",
    10: "changos",
}

V1_KEY = {
    1: "casa",
    2: "departamento",
    3: "pieza_vivienda",
    4: "mejora_mediagua",
    5: "rancho_ruca",
    6: "materiales_precarios",
    7: "otro_tipo",
    8: "hospederia",
    9: "caleta_calle",
    10: "vivienda_colectiva",
    11: "residencial_pension",
}

V2_KEY = {
    1: "propio_pagado",
    2: "arrendado",
    3: "cedido",
    4: "usufructo",
    5: "ocupacion_irregular",
    6: "poseedor_irregular",
}

V4_KEY = {
    1: "agua_medidor_propio",
    2: "agua_medidor_compartido",
    3: "agua_sin_medidor",
    4: "pozo_noria",
    5: "rio_vertiente",
    6: "otra_fuente_no_potable",
}

# Educación
E1_KEY = {1: "asiste_si", 2: "asiste_no"}

E2_KEY = {
    1: "no_necesario",
    2: "problemas_acceso",
    3: "problemas_traslado",
    4: "problemas_economicos",
    5: "quehaceres_cuidado",
    6: "embarazo_maternidad",
    7: "enfermedad_inhabilita",
    8: "problemas_familiares",
    9: "no_le_interesa",
    10: "esta_trabajando",
    11: "termino_estudiar",
    12: "otra_razon",
}

E3_KEY = {
    1: "ninguno",
    2: "parvularia",
    3: "basica",
    4: "preparatoria_antigua",
    5: "media_ch",
    6: "media_tp",
    7: "humanidades_antiguo",
    8: "tecnica_antigua",
    9: "cft_incompleta",
    10: "cft_completa",
    11: "ip_incompleta",
    12: "ip_completa",
    13: "univ_incompleta",
    14: "univ_completa",
    15: "postgrado",
    16: "especial_diferencial",
}


# ============================================================
#                API PRINCIPAL RSH
# ============================================================

@csrf_exempt


def api_rsh(request):

    print("\n================ DEBUG API RSH ================")
    print("Raw body:", request.body)

    # ----------- PARSE JSON -----------
    try:
        body = json.loads(request.body)
    except Exception as e:
        print("❌ ERROR PARSEANDO JSON:", e)
        return JsonResponse({"error": "JSON inválido"}, status=400)

    print("Parsed BODY:", body)

    categoria = body.get("categoria")
    filtros = body.get("filtros", {})

    uvec_list = body.get("uvec", [])
    sb_list = body.get("sb", [])
    omz_list = body.get("omz", [])

    print("MODO UV:", uvec_list)
    print("MODO SB:", sb_list)
    print("MODO OMZ:", omz_list)
    print("CATEGORIA:", categoria)

    # Query base
    qs_base = Datos.objects.select_related("uvec").all()

    # --------------------------------------------------------
    # MODO UV (1 sola fila)
    # --------------------------------------------------------
    if uvec_list:
        print("=== MODO UV ===")

        resultados = []

        for cod in uvec_list:

            qs_uv = qs_base.filter(uvec__cod_uv=cod)

            resumen = _procesar_resumen(
                qs_uv,
                categoria,
                filtros,
                etiqueta="uvec",
                valor=cod
            )

            resultados.append(resumen)

        return JsonResponse(resultados, safe=False)
    
    # --------------------------------------------------------
    # MODO SB — varias filas (una por SB seleccionado)
    # --------------------------------------------------------
    if sb_list:
        print("=== MODO SB ===")

        resultados = []

        for sbid in sb_list:

            qs_sb = qs_base.filter(uvec__id_sb_id=sbid)

            # nombre real del SB
            sb_obj = Sb.objects.filter(id=sbid).first()
            sb_nombre = sb_obj.nombre if sb_obj else f"SB {sbid}"

            resumen = _procesar_resumen(
                qs_sb,
                categoria,
                filtros,
                etiqueta="sb",
                valor=sb_nombre
            )

            resultados.append(resumen)

        return JsonResponse(resultados, safe=False)

    # --------------------------------------------------------
    # MODO OMZ — varias filas (una por OMZ seleccionada)
    # --------------------------------------------------------
    if omz_list:
        print("=== MODO OMZ ===")

        resultados = []

        for omzid in omz_list:

            qs_omz = qs_base.filter(uvec__id_sb__id_omz_id=omzid)

            # nombre real OMZ
            omz_obj = Omz.objects.filter(id=omzid).first()
            omz_nombre = omz_obj.nombre if omz_obj else f"OMZ {omzid}"

            resumen = _procesar_resumen(
                qs_omz,
                categoria,
                filtros,
                etiqueta="omz",
                valor=omz_nombre
            )

            resultados.append(resumen)

        return JsonResponse(resultados, safe=False)

    # --------------------------------------------------------
    # MODO COMUNAL (ningún UV, ningún SB, ningún OMZ)
    # --------------------------------------------------------
    print("=== MODO COMUNAL ===")

    resumen = _procesar_resumen(
        qs_base,
        categoria,
        filtros,
        etiqueta="comuna",
        valor="Comunal"
    )

    return JsonResponse([resumen], safe=False)


# ======================================================================
# 🔥 FUNCIÓN UNIFICADA PARA PROCESAR CUALQUIER MODO (UV, SB, OMZ o Comunal)
# ======================================================================
def _procesar_resumen(qs, categoria, filtros, etiqueta, valor):
    """
    Construye la fila de resultados para:
    - UV
    - SB
    - OMZ
    - Comunal
    """

    resumen = {etiqueta: valor}

    # Total
    total = qs.count()
    filtros_aplicados = any(len(v) for v in filtros.values())

    # Solo mostramos total si NO hay filtros (excepto HABITANTE)
    if categoria != "habitante" and not filtros_aplicados:
        resumen["total"] = total

    # =========================================
    # HABITANTE
    # =========================================
    if categoria == "habitante":

        for v in filtros.get("socio", []):

            if v == "habitantes_total":
                resumen["habitantes_total"] = total

            elif v.startswith("sexo_"):
                sex = int(v.split("_")[1])
                key = "sexo_m" if sex == 1 else "sexo_f"
                resumen[key] = qs.filter(sexo=sex).count()

            elif v.startswith("nacionalidad_"):
                n = int(v.split("_")[1])
                key = "nacionalidad_ch" if n == 1 else "nacionalidad_ex"
                resumen[key] = qs.filter(nacionalidad_id=n).count()

        for v in filtros.get("parentescoid", []):
            key = PARENTESCO_KEY.get(v)
            if key:
                resumen[key] = qs.filter(parentescoid=v).count()

        for v in filtros.get("indigena", []):
            key = INDIGENA_KEY.get(v)
            if key:
                resumen[key] = qs.filter(indigena=v).count()

        for v in filtros.get("tramo", []):
            resumen[f"tramo_{v}"] = qs.filter(tramo=v).count()

        return resumen

    # =========================================
    # VIVIENDA
    # =========================================
    if categoria == "vivienda":

        for v in filtros.get("v1", []):
            key = V1_KEY.get(v)
            if key:
                resumen[key] = qs.filter(v1=v).count()

        for v in filtros.get("v2", []):
            key = V2_KEY.get(v)
            if key:
                resumen[key] = qs.filter(v2=v).count()

        for v in filtros.get("v4", []):
            key = V4_KEY.get(v)
            if key:
                resumen[key] = qs.filter(v4=v).count()

        return resumen

    # =========================================
    # EDUCACIÓN
    # =========================================
    if categoria == "educacion":

        for v in filtros.get("e1", []):
            key = E1_KEY.get(v)
            resumen[key] = qs.filter(e1=v).count()

        for v in filtros.get("e2", []):
            key = E2_KEY.get(v)
            resumen[key] = qs.filter(e2=v).count()

        for v in filtros.get("e3", []):
            key = E3_KEY.get(v)
            resumen[key] = qs.filter(e3=v).count()

        return resumen

    # =========================================
    # SALUD
    # =========================================
    if categoria == "salud":

        for campo in filtros.get("salud", []):
            if campo in SALUD_KEY:
                key = SALUD_KEY[campo]
                resumen[key] = qs.filter(**{campo: 1}).count()

        return resumen

    # =========================================
    # OCUPACION
    # =========================================
    if categoria == "ocupacion":

        for v in filtros.get("o1", []):
            key = O1_KEY.get(v)
            resumen[key] = qs.filter(o1=v).count()

        for v in filtros.get("o2", []):
            key = O2_KEY.get(v)
            resumen[key] = qs.filter(o2=v).count()

        for v in filtros.get("o3", []):
            key = O3_KEY.get(v)
            resumen[key] = qs.filter(o3=v).count()

        for v in filtros.get("o4", []):
            key = O4_KEY.get(v)
            resumen[key] = qs.filter(o4=v).count()

        for v in filtros.get("o5", []):
            key = O5_KEY.get(v)
            resumen[key] = qs.filter(o5=v).count()

        for v in filtros.get("o6", []):
            key = O6_KEY.get(v)
            resumen[key] = qs.filter(o6=v).count()

        for v in filtros.get("o7", []):
            key = O7_KEY.get(v)
            resumen[key] = qs.filter(o7=v).count()

        for v in filtros.get("o8", []):
            key = O8_KEY.get(v)
            resumen[key] = qs.filter(o8=v).count()

        for v in filtros.get("o9", []):
            key = O9_KEY.get(v)
            resumen[key] = qs.filter(o9=v).count()

        return resumen
