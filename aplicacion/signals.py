from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Bloquear, Permitir, Ping, RegistroActividad

@receiver(post_save, sender=Bloquear)
def registrar_accion_bloquear(sender, instance, created, **kwargs):
    if created:
        accion = "Bloquear creado"
    else:
        accion = "Bloquear modificado"
    RegistroActividad.objects.create(
        usuario=instance.usuario,
        accion=accion,
        modelo_afectado="Bloquear"
    )

@receiver(post_save, sender=Permitir)
def registrar_accion_permitir(sender, instance, created, **kwargs):
    if created:
        accion = "Permitir creado"
    else:
        accion = "Permitir modificado"
    RegistroActividad.objects.create(
        usuario=instance.usuario,
        accion=accion,
        modelo_afectado="Permitir"
    )

@receiver(post_save, sender=Ping)
def registrar_accion_ping(sender, instance, created, **kwargs):
    if created:
        accion = "Ping creado"
    else:
        accion = "Ping modificado"
    RegistroActividad.objects.create(
        usuario=instance.usuario,
        accion=accion,
        modelo_afectado="Ping"
    )

@receiver(post_delete, sender=Bloquear)
def registrar_eliminacion_bloquear(sender, instance, **kwargs):
    RegistroActividad.objects.create(
        usuario=instance.usuario,
        accion="Bloquear eliminado",
        modelo_afectado="Bloquear"
    )
