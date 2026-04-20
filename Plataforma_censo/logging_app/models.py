from django.db import models

class RegistroAcceso(models.Model):

    email = models.EmailField()
    panel = models.CharField(max_length=100)  # CENSO, RSH, ACCESO

    tipo = models.CharField(max_length=50, null=True, blank=True)  
    # acceso / consulta

    parametros = models.JSONField(null=True, blank=True)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.panel} - {self.tipo}"