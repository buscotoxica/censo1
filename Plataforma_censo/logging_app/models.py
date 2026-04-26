from django.db import models

class RegistroAcceso(models.Model):
    email = models.EmailField()
    panel = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, null=True, blank=True)
    parametros = models.JSONField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.panel} - {self.tipo}"


class CorreoBloqueado(models.Model):
    email = models.EmailField()
    ip = models.CharField(max_length=50, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.ip} - {self.fecha}"


class IPBloqueada(models.Model):
    ip = models.CharField(max_length=50, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    bloqueos = models.IntegerField(default=1)
    permanente = models.BooleanField(default=False)
    hasta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.ip} - {'PERMANENTE' if self.permanente else str(self.hasta)}"