# tu_app/management/commands/configurar_nftables.py
from django.core.management.base import BaseCommand
from scripts.nftables import configurar_nftables

class Command(BaseCommand):
    help = 'Configura nftables basado en las reglas de bloqueo de la base de datos.'

    def handle(self, *args, **kwargs):
        try:
            configurar_nftables()
            self.stdout.write(self.style.SUCCESS('Nftables configurado exitosamente.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al configurar nftables: {str(e)}'))
