from django.contrib import admin
from .models import Permitir, Ping, Bloquear, DNSQuery, RegistroActividad
import csv
from django.http import HttpResponse
import subprocess
import os
from django.contrib import messages
from django.urls import path
from django.http import HttpResponseRedirect



class BloquearAdmin(admin.ModelAdmin):
    verbose_name = "Bloquear tráfico"
    verbose_name_plural = "Bloqueos de tráfico"
    
    # Define qué columnas se mostrarán en el listado del admin
    list_display = ('usuario', 'port', 'domain', 'action')  # Añade aquí los campos que quieres mostrar

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Ejecutar el script como root
        script_path = os.path.join(os.path.dirname(__file__), '/var/www/html/myproject_backup/Run.sh')
        try:
            subprocess.run(['sudo', 'sh', script_path], check=True)
        except subprocess.CalledProcessError as e:
            self.message_user(request, f'Error al ejecutar el script: {e}', level='error')

admin.site.register(Bloquear, BloquearAdmin)

class PermitirAdmin(admin.ModelAdmin):
    verbose_name = "Permitir tráfico"
    verbose_name_plural = "Permitir tráfico"
    
    # Define qué columnas se mostrarán en el listado del admin
    list_display = ('usuario', 'port', 'domain', 'action')  # Asegúrate de que estos campos existan en el modelo Permitir

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Ejecutar el script como root
        script_path = os.path.join(os.path.dirname(__file__), '/var/www/html/myproject_backup/add.sh')
        try:
            # Ejecución del script con permisos de root
            subprocess.run(['sudo', 'sh', script_path], check=True)
        except subprocess.CalledProcessError as e:
            self.message_user(request, f'Error al ejecutar el script: {e}', level='error')

admin.site.register(Permitir, PermitirAdmin)

#Dns
class DNSQueryAdmin(admin.ModelAdmin):
    list_display = ['domain', 'ip_address', 'timestamp']
    
    def save_model(self, request, obj, form, change):
        if not obj.ip_address:
            # Realizar la consulta DNS usando nslookup
            result = subprocess.run(['nslookup', obj.domain], stdout=subprocess.PIPE, text=True)
            output_lines = result.stdout.splitlines()
            ip_address = None
            for line in output_lines:
                if 'Address: ' in line:
                    ip_address = line.split('Address: ')[1].strip()
                    break
            obj.ip_address = ip_address

        super().save_model(request, obj, form, change)

    verbose_name = "Consulta DNS"
    verbose_name_plural = "Consultas DNS"
admin.site.register(DNSQuery, DNSQueryAdmin)

#actividades
class RegistroActividadAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'modelo_afectado', 'fecha')
    list_filter = ('usuario', 'modelo_afectado', 'fecha')

    verbose_name = "Registro de actividad"
    verbose_name_plural = "Registros de actividades"

admin.site.register(RegistroActividad, RegistroActividadAdmin)


#Protocolo
class PingAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'ip', 'protocolo')
    list_filter = ('timestamp', 'protocolo')

    # Sobrescribir el método para la vista de lista y pasar un contexto personalizado
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super(PingAdmin, self).changelist_view(request, extra_context=extra_context)

    # Definir la vista personalizada para activar el protocolo
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('activar-protocolo/', self.admin_site.admin_view(self.activar_protocolo), name='activar_protocolo'),
        ]
        return custom_urls + urls

    # Acción para activar el protocolo (ejecutar el script)
    def activar_protocolo(self, request):
        script_path = '/var/www/html/myproject_backup/log.sh'  # Ruta al script

        try:
            # Ejecutar el script .sh usando sudo
            subprocess.run(['sudo', 'sh', script_path], check=True)
            # Mostrar un mensaje de éxito en la interfaz del administrador
            self.message_user(request, "Protocolo activado con éxito.", level=messages.SUCCESS)
        except subprocess.CalledProcessError as e:
            # Si ocurre un error, enviar un mensaje de error al administrador
            self.message_user(request, f'Error al activar el protocolo: {e}', level=messages.ERROR)

        # Redirigir de vuelta a la página de la lista de registros
        return HttpResponseRedirect("../")

    activar_protocolo.short_description = "Activar Protocolo"

# Registrar el modelo en el admin
admin.site.register(Ping, PingAdmin)