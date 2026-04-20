from django.db import models


class Datos(models.Model):
    id = models.AutoField(primary_key=True)
    folio = models.IntegerField(null=True, blank=True)
    uvec = models.ForeignKey('censo.Uv', on_delete=models.RESTRICT, db_column='uvec')

    tramo = models.IntegerField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    parentescoid = models.IntegerField(null=True, blank=True)
    numpareja = models.IntegerField(null=True, blank=True)
    indigena = models.IntegerField(null=True, blank=True)

    # Variables v1–v11_e
    v1 = models.IntegerField(null=True, blank=True)
    v2 = models.IntegerField(null=True, blank=True)
    v3 = models.IntegerField(null=True, blank=True)
    v4 = models.IntegerField(null=True, blank=True)
    v5 = models.IntegerField(null=True, blank=True)
    v6 = models.IntegerField(null=True, blank=True)
    v7 = models.IntegerField(null=True, blank=True)
    v8 = models.IntegerField(null=True, blank=True)
    v9 = models.IntegerField(null=True, blank=True)
    v9_e = models.IntegerField(null=True, blank=True)
    v10 = models.IntegerField(null=True, blank=True)
    v10_e = models.IntegerField(null=True, blank=True)
    v11 = models.IntegerField(null=True, blank=True)
    v11_e = models.IntegerField(null=True, blank=True)

    # e1-e4
    e1 = models.IntegerField(null=True, blank=True)
    e2 = models.IntegerField(null=True, blank=True)
    e3 = models.IntegerField(null=True, blank=True)
    e4 = models.IntegerField(null=True, blank=True)

    # s1-s2
    s1a = models.IntegerField(null=True, blank=True)
    s1b = models.IntegerField(null=True, blank=True)
    s1c = models.IntegerField(null=True, blank=True)
    s1d = models.IntegerField(null=True, blank=True)
    s1e = models.IntegerField(null=True, blank=True)
    s1f = models.IntegerField(null=True, blank=True)

    s2a = models.IntegerField(null=True, blank=True)
    s2b = models.IntegerField(null=True, blank=True)
    s2c = models.IntegerField(null=True, blank=True)
    s2d = models.IntegerField(null=True, blank=True)
    s2e = models.IntegerField(null=True, blank=True)

    # o1-o9
    o1 = models.IntegerField(null=True, blank=True)
    o2 = models.IntegerField(null=True, blank=True)
    o3 = models.IntegerField(null=True, blank=True)
    o4 = models.IntegerField(null=True, blank=True)
    o5 = models.IntegerField(null=True, blank=True)
    o6 = models.IntegerField(null=True, blank=True)
    o7 = models.IntegerField(null=True, blank=True)
    o8 = models.IntegerField(null=True, blank=True)
    o9 = models.IntegerField(null=True, blank=True)

    y1 = models.IntegerField(null=True, blank=True)
    y2 = models.IntegerField(null=True, blank=True)
    y3 = models.IntegerField(null=True, blank=True)

    informante = models.IntegerField(null=True, blank=True)
    fecha_encuesta = models.IntegerField(null=True, blank=True)
    fecha_modificacion = models.IntegerField(null=True, blank=True)
    c_zona = models.IntegerField(null=True, blank=True)
    sexo = models.IntegerField(null=True, blank=True)
    fechanacimiento = models.IntegerField(null=True, blank=True)
    nacionalidad_id = models.IntegerField(null=True, blank=True)
    fecha_calificacion = models.IntegerField(null=True, blank=True)

    periodo_rsh = models.CharField(max_length=10, null=True, blank=True)
    c_calle_fps = models.CharField(max_length=50, null=True, blank=True)
    n_calle_uni_rsh = models.CharField(max_length=255, null=True, blank=True)
    tipo_ah = models.CharField(max_length=10, null=True, blank=True)
    c_cod_ah_fps = models.IntegerField(null=True, blank=True)
    c_ah_nom = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'datos'
        managed = False