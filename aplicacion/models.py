from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import subprocess
from django.utils import timezone
from django.core.exceptions import ValidationError

class Permitir(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=1)
    port = models.PositiveIntegerField(blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True)
    action = models.CharField(max_length=20, blank=True) 

    class Meta:
        verbose_name = "Permitir tráfico"
        verbose_name_plural = "Permitir tráfico"

    def __str__(self):
        return f"{self.domain} (Port: {self.port})"  # Cambia según lo que quieras mostrar

class Bloquear(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=1)
    port = models.PositiveIntegerField(blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True)
    action = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Bloquear tráfico"
        verbose_name_plural = "Bloqueos de tráfico"

    def __str__(self):
        # Cambia esto según lo que quieras que se muestre en el admin
        return f"{self.domain} (Port: {self.port})"  # Muestra el dominio y el puerto

class Ping(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    ip = models.GenericIPAddressField()
    mensaje = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Nuevo campo para almacenar el protocolo
    protocolo = models.CharField(max_length=10, null=True, blank=True)

    def clean(self):
        if self.timestamp is None:
            raise ValidationError('El campo timestamp no puede ser nulo.')

    def __str__(self):
        return f"{self.ip} - {self.protocolo}"
    
    class Meta:
        verbose_name = "Protocolo"
        verbose_name_plural = "Protocolos"
        
class DNSQuery(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=1)
    domain = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'{self.domain} - {self.ip_address}'
    
    class Meta:
        verbose_name = "Consulta Dns"
        verbose_name_plural = "Consultas Dns"

#admin
class RegistroActividad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=1)
    accion = models.CharField(max_length=255)
    modelo_afectado = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.fecha}"
    
    class Meta:
        verbose_name = "Registro de actividad"
        verbose_name_plural = "Registro de actividades"
    


