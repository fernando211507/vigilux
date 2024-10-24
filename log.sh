#!/bin/bash

# Ruta al archivo JSON de logs de Suricata
LOG_FILE="/var/log/suricata/eve.json"

# Contar registros a procesar (en este caso, los primeros 100)
jq -c '. | select(.alert.signature == "Ping detectado")' "$LOG_FILE" | head -n 50 | while read -r linea; do
    # Extraer campos específicos de la línea (timestamp, src_ip, mensaje, usuario, protocolo)
    timestamp=$(echo "$linea" | jq -r '.timestamp')
    ip=$(echo "$linea" | jq -r '.src_ip')
    mensaje=$(echo "$linea" | jq -r '.alert.signature')
    
    # Extraer el campo 'usuario'. Si no está presente, usar un valor por defecto
    usuario=$(echo "$linea" | jq -r '.usuario // "default_user"')
    
    # Extraer el campo 'protocol'. Si no está presente, usar 'unknown'
    protocolo=$(echo "$linea" | jq -r '.proto // "unknown"')

    # Insertar en la base de datos
    sqlite3 nftables_data.db "INSERT INTO aplicacion_ping (timestamp, ip, mensaje, usuario_id, protocolo) VALUES ('$timestamp', '$ip', '$mensaje', '$usuario', '$protocolo');"
done

echo "50 registros de pings insertados en la base de datos"
