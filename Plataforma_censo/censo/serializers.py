from rest_framework import serializers
from .models import Omz, Sb, Uv, Censo, CensoUv


class OmzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Omz
        fields = ['id', 'nombre']


class SbSerializer(serializers.ModelSerializer):
    omz = OmzSerializer(source='id_omz', read_only=True)

    class Meta:
        model = Sb
        fields = ['id', 'nombre', 'id_omz', 'omz']


class UvSerializer(serializers.ModelSerializer):
    sb = SbSerializer(source='id_sb', read_only=True)

    class Meta:
        model = Uv
        fields = ['cod_uv', 'id_sb', 'sb']


class CensoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Censo
        fields = ['id', 'annio']


class CensoUvSerializer(serializers.ModelSerializer):
    uv = UvSerializer(source='id_uv', read_only=True)
    censo = CensoSerializer(source='id_censo', read_only=True)

    class Meta:
        model = CensoUv
        fields = [
            'id', 'id_censo', 'id_uv',
            'area', 'total_pers', 'densidad', 'total_vivi',
            'hombres', 'mujeres',
            # 2017
            'edad_0a5', 'edad_6a14', 'edad_15a64', 'edad_64ymas',
            # 2024
            'edad_0_a_5', 'edad_6_a_13', 'edad_14_a_17',
            'edad_18_a_24', 'edad_25_a_44',
            'edad_45_a_59', 'edad_60_o_mas',
            'iam', 'idd',
            'uv', 'censo',
            # empleo  situación laboral
            'no_sabe_leer', 'ocupadas', 'desocupadas',
            'fuera_fuerza_trabajo', 'ocupadas_independientes',
            'ocupadas_dependientes', 'ocupadas_no_remunerados',
            # empleo  ocupación
            'ocup_directores', 'ocup_profesionales', 'ocup_tecnicos',
            'ocup_apoyo_admin', 'ocup_servicios_vendedores',
            'ocup_agricultores', 'ocup_artesanos', 'ocup_operadores',
            'ocup_elementales', 'ocup_fuerzas_armadas',
            # empleo  rama
            'rama_agricultura', 'rama_mineria', 'rama_manufactura',
            'rama_electricidad', 'rama_agua', 'rama_construccion',
            'rama_comercio', 'rama_transporte', 'rama_alojamiento',
            'rama_info_comunicaciones', 'rama_financiero', 'rama_inmobiliario',
            'rama_profesional', 'rama_servicios_admin', 'rama_adm_publica',
            'rama_ensenanza', 'rama_salud', 'rama_artistico',
            'rama_otros_servicios', 'rama_hogares', 'rama_extraterritorial',
            # vivienda  tenencia
            'ten_propia_pagada', 'ten_propia_pagandose',
            'ten_arrendada_contrato', 'ten_arrendada_sin_contrato',
            'ten_cedida_trabajo', 'ten_cedida_familiar', 'ten_otro',
            # vivienda  tipo
            'viv_particulares', 'viv_particulares_ocupadas',
            'viv_particulares_desocupadas', 'viv_casa', 'viv_depto',
            'viv_indigena', 'viv_pieza', 'viv_mediagua', 'viv_movil', 'viv_otro',
            # vivienda  déficit
            'n_viv_hacinadas', 'n_viv_irrecuperables',
            'n_hog_allegados', 'n_nucleos_hacinados',
            # materialidad  paredes
            'par_hormigon','par_albanileria','par_tabique_forrado',
            'par_tabique_sin_forro','par_artesanal','par_precarios',
# materialidad  techo
            'techo_tejas','techo_hormigon','techo_zinc','techo_fibrocemento',
            'techo_fonolita','techo_paja','techo_precarios','techo_sin_cubierta',
# materialidad  piso
            'piso_radier_con','piso_radier_sin','piso_baldosa',
            'piso_capa_cemento','piso_tierra',
            'esc_promedio', 'esc_parvularia', 'esc_basica', 'esc_media', 'esc_superior',
            'n_fuente_agua_publica', 'n_fuente_agua_pozo',
            'n_fuente_agua_camion', 'n_fuente_agua_rio',
            'n_distrib_agua_llave', 'n_distrib_agua_llave_fuera',
            'n_distrib_agua_acarreo',
            # saneamiento
            'n_serv_hig_alc_dentro', 'n_serv_hig_alc_fuera',
            'n_serv_hig_fosa', 'n_serv_hig_pozo',
            'n_serv_hig_acequia_canal', 'n_serv_hig_cajon_otro',
            'n_serv_hig_bano_quimico', 'n_serv_hig_bano_seco',
            'n_serv_hig_no_tiene',
            # electricidad
            'n_fuente_elect_publica', 'n_fuente_elect_diesel',
            'n_fuente_elect_solar', 'n_fuente_elect_eolica',
            'n_fuente_elect_otro', 'n_fuente_elect_no_tiene',
            # basura
            'n_basura_servicios', 'n_basura_entierra',
            'n_basura_eriazo', 'n_basura_rio', 'n_basura_otro',
        ]