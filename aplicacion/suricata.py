
import os
import re
from datetime import datetime
from .models import Alerta  # Importa tu modelo Alerta

logfile_path = '/var/log/suricata/suricata.log'  # Ruta al archivo de registros de Suricata

def parse_suricata_logs():
    with open(logfile_path, 'r') as logfile:
        for line in logfile:
            # Supongamos que el formato de las alertas es: [timestamp] mensaje
            match = re.match(r'\[(.*?)\]\s(.*)', line)
            if match:
                timestamp_str, message = match.groups()
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                
                # Crea una instancia de Alerta y guárdala en la base de datos
                alert = Alerta(timestamp=timestamp, message=message)
                alert.save()

if __name__ == "__main__":
    parse_suricata_logs()
