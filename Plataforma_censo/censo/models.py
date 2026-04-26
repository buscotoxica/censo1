from django.db import models


class Omz(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'omz'
        managed = True

    def __str__(self):
        return self.nombre



class Sb(models.Model):
    id = models.AutoField(primary_key=True)
    id_omz = models.ForeignKey('Omz', on_delete=models.CASCADE, db_column='id_omz')
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'sb'
        managed = True

    def __str__(self):
        return self.nombre



class Uv(models.Model):
    cod_uv = models.CharField(primary_key=True, max_length=255)
    id_sb = models.ForeignKey('Sb', on_delete=models.CASCADE, db_column='id_sb')

    class Meta:
        db_table = 'uv'
        managed = True

    def __str__(self):
        return self.cod_uv


class Censo(models.Model):
    id = models.AutoField(primary_key=True)
    annio = models.IntegerField()

    class Meta:
        db_table = 'censo'
        managed = True

    def __str__(self):
        return str(self.annio)



class CensoUv(models.Model):
    id = models.AutoField(primary_key=True)
    id_censo = models.ForeignKey('Censo', on_delete=models.CASCADE, db_column='id_censo')
    id_uv = models.ForeignKey('Uv', on_delete=models.CASCADE, db_column='id_uv')

    area = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    total_pers = models.IntegerField(null=True, blank=True)
    densidad = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    total_vivi = models.IntegerField(null=True, blank=True)
    hombres = models.IntegerField(null=True, blank=True)
    mujeres = models.IntegerField(null=True, blank=True)

    edad_0a5 = models.IntegerField(null=True, blank=True)
    edad_6a14 = models.IntegerField(null=True, blank=True)
    edad_15a64 = models.IntegerField(null=True, blank=True)
    edad_64ymas = models.IntegerField(null=True, blank=True)

    iam = models.IntegerField(null=True, blank=True)
    idd = models.IntegerField(null=True, blank=True)
    edad_0_a_5 = models.IntegerField(null=True, blank=True)
    edad_6_a_13 = models.IntegerField(null=True, blank=True)
    edad_14_a_17 = models.IntegerField(null=True, blank=True)
    edad_18_a_24 = models.IntegerField(null=True, blank=True)
    edad_25_a_44 = models.IntegerField(null=True, blank=True)
    edad_45_a_59 = models.IntegerField(null=True, blank=True)
    edad_60_o_mas = models.IntegerField(null=True, blank=True)
    no_sabe_leer = models.IntegerField(null=True, blank=True)
    ocupadas = models.IntegerField(null=True, blank=True)
    desocupadas = models.IntegerField(null=True, blank=True)
    fuera_fuerza_trabajo = models.IntegerField(null=True, blank=True)
    ocupadas_independientes = models.IntegerField(null=True, blank=True)
    ocupadas_dependientes = models.IntegerField(null=True, blank=True)
    ocupadas_no_remunerados = models.IntegerField(null=True, blank=True)

# Empleo  ocupación
    ocup_directores = models.IntegerField(null=True, blank=True)
    ocup_profesionales = models.IntegerField(null=True, blank=True)
    ocup_tecnicos = models.IntegerField(null=True, blank=True)
    ocup_apoyo_admin = models.IntegerField(null=True, blank=True)
    ocup_servicios_vendedores = models.IntegerField(null=True, blank=True)
    ocup_agricultores = models.IntegerField(null=True, blank=True)
    ocup_artesanos = models.IntegerField(null=True, blank=True)
    ocup_operadores = models.IntegerField(null=True, blank=True)
    ocup_elementales = models.IntegerField(null=True, blank=True)
    ocup_fuerzas_armadas = models.IntegerField(null=True, blank=True)

# Empleo  rama de actividad
    rama_agricultura = models.IntegerField(null=True, blank=True)
    rama_mineria = models.IntegerField(null=True, blank=True)
    rama_manufactura = models.IntegerField(null=True, blank=True)
    rama_electricidad = models.IntegerField(null=True, blank=True)
    rama_agua = models.IntegerField(null=True, blank=True)
    rama_construccion = models.IntegerField(null=True, blank=True)
    rama_comercio = models.IntegerField(null=True, blank=True)
    rama_transporte = models.IntegerField(null=True, blank=True)
    rama_alojamiento = models.IntegerField(null=True, blank=True)
    rama_info_comunicaciones = models.IntegerField(null=True, blank=True)
    rama_financiero = models.IntegerField(null=True, blank=True)
    rama_inmobiliario = models.IntegerField(null=True, blank=True)
    rama_profesional = models.IntegerField(null=True, blank=True)
    rama_servicios_admin = models.IntegerField(null=True, blank=True)
    rama_adm_publica = models.IntegerField(null=True, blank=True)
    rama_ensenanza = models.IntegerField(null=True, blank=True)
    rama_salud = models.IntegerField(null=True, blank=True)
    rama_artistico = models.IntegerField(null=True, blank=True)
    rama_otros_servicios = models.IntegerField(null=True, blank=True)
    rama_hogares = models.IntegerField(null=True, blank=True)
    rama_extraterritorial = models.IntegerField(null=True, blank=True)
    # vivienda  tenencia
    ten_propia_pagada            = models.IntegerField(null=True, blank=True)
    ten_propia_pagandose         = models.IntegerField(null=True, blank=True)
    ten_arrendada_contrato       = models.IntegerField(null=True, blank=True)
    ten_arrendada_sin_contrato   = models.IntegerField(null=True, blank=True)
    ten_cedida_trabajo           = models.IntegerField(null=True, blank=True)
    ten_cedida_familiar          = models.IntegerField(null=True, blank=True)
    ten_otro                     = models.IntegerField(null=True, blank=True)
# vivienda  tipo
    viv_particulares             = models.IntegerField(null=True, blank=True)
    viv_particulares_ocupadas    = models.IntegerField(null=True, blank=True)
    viv_particulares_desocupadas = models.IntegerField(null=True, blank=True)
    viv_casa                     = models.IntegerField(null=True, blank=True)
    viv_depto                    = models.IntegerField(null=True, blank=True)
    viv_indigena                 = models.IntegerField(null=True, blank=True)
    viv_pieza                    = models.IntegerField(null=True, blank=True)
    viv_mediagua                 = models.IntegerField(null=True, blank=True)
    viv_movil                    = models.IntegerField(null=True, blank=True)
    viv_otro                     = models.IntegerField(null=True, blank=True)
# vivienda  déficit
    n_viv_hacinadas              = models.IntegerField(null=True, blank=True)
    n_viv_irrecuperables         = models.IntegerField(null=True, blank=True)
    n_hog_allegados              = models.IntegerField(null=True, blank=True)
    n_nucleos_hacinados          = models.IntegerField(null=True, blank=True)
    par_hormigon          = models.IntegerField(null=True, blank=True)
    par_albanileria       = models.IntegerField(null=True, blank=True)
    par_tabique_forrado   = models.IntegerField(null=True, blank=True)
    par_tabique_sin_forro = models.IntegerField(null=True, blank=True)
    par_artesanal         = models.IntegerField(null=True, blank=True)
    par_precarios         = models.IntegerField(null=True, blank=True)
# materialidad  techo
    techo_tejas           = models.IntegerField(null=True, blank=True)
    techo_hormigon        = models.IntegerField(null=True, blank=True)
    techo_zinc            = models.IntegerField(null=True, blank=True)
    techo_fibrocemento    = models.IntegerField(null=True, blank=True)
    techo_fonolita        = models.IntegerField(null=True, blank=True)
    techo_paja            = models.IntegerField(null=True, blank=True)
    techo_precarios       = models.IntegerField(null=True, blank=True)
    techo_sin_cubierta    = models.IntegerField(null=True, blank=True)
# materialidad  piso
    piso_radier_con       = models.IntegerField(null=True, blank=True)
    piso_radier_sin       = models.IntegerField(null=True, blank=True)
    piso_baldosa          = models.IntegerField(null=True, blank=True)
    piso_capa_cemento     = models.IntegerField(null=True, blank=True)
    piso_tierra           = models.IntegerField(null=True, blank=True)    
    # educación
    esc_promedio   = models.IntegerField(null=True, blank=True)
    esc_parvularia = models.IntegerField(null=True, blank=True)
    esc_basica     = models.IntegerField(null=True, blank=True)
    esc_media      = models.IntegerField(null=True, blank=True)
    esc_superior   = models.IntegerField(null=True, blank=True)
    n_fuente_agua_publica = models.IntegerField(null=True, blank=True)
    n_fuente_agua_pozo = models.IntegerField(null=True, blank=True)
    n_fuente_agua_camion = models.IntegerField(null=True, blank=True)
    n_fuente_agua_rio = models.IntegerField(null=True, blank=True)
    n_distrib_agua_llave = models.IntegerField(null=True, blank=True)
    n_distrib_agua_llave_fuera = models.IntegerField(null=True, blank=True)
    n_distrib_agua_acarreo = models.IntegerField(null=True, blank=True)
# saneamiento
    n_serv_hig_alc_dentro = models.IntegerField(null=True, blank=True)
    n_serv_hig_alc_fuera = models.IntegerField(null=True, blank=True)
    n_serv_hig_fosa = models.IntegerField(null=True, blank=True)
    n_serv_hig_pozo = models.IntegerField(null=True, blank=True)
    n_serv_hig_acequia_canal = models.IntegerField(null=True, blank=True)
    n_serv_hig_cajon_otro = models.IntegerField(null=True, blank=True)
    n_serv_hig_bano_quimico = models.IntegerField(null=True, blank=True)
    n_serv_hig_bano_seco = models.IntegerField(null=True, blank=True)
    n_serv_hig_no_tiene = models.IntegerField(null=True, blank=True)
# electricidad
    n_fuente_elect_publica = models.IntegerField(null=True, blank=True)
    n_fuente_elect_diesel = models.IntegerField(null=True, blank=True)
    n_fuente_elect_solar = models.IntegerField(null=True, blank=True)
    n_fuente_elect_eolica = models.IntegerField(null=True, blank=True)
    n_fuente_elect_otro = models.IntegerField(null=True, blank=True)
    n_fuente_elect_no_tiene = models.IntegerField(null=True, blank=True)
# basura
    n_basura_servicios = models.IntegerField(null=True, blank=True)
    n_basura_entierra = models.IntegerField(null=True, blank=True)
    n_basura_eriazo = models.IntegerField(null=True, blank=True)
    n_basura_rio = models.IntegerField(null=True, blank=True)
    n_basura_otro = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'censo_uv'
        managed = True

class RegistroConsulta(models.Model):
    microservicio = models.CharField(max_length=100)
    email_usuario = models.CharField(max_length=255, blank=True, null=True)
    fecha_consulta = models.DateTimeField(auto_now_add=True)
    parametros = models.TextField()

    class Meta:
        db_table = 'registro_consulta'
        managed = True

    def __str__(self):
        return f"{self.microservicio} - {self.fecha_consulta:%Y-%m-%d %H:%M}"