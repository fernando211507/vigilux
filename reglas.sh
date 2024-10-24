#!/bin/bash

# Ruta al comando nft
NFT_CMD="/usr/sbin/nft"

# Obtener datos de la base de datos SQLite
while IFS='|' read -r port domain action; do
    # Lógica para crear reglas en nftables usando los datos obtenidos
    if [ -n "$port" ]; then
        # Crear regla para bloquear puerto
        $NFT_CMD add rule filter input tcp dport "$port" drop
        echo "Bloqueando puerto: $port"
    fi

    if [ -n "$domain" ]; then
        # Crear regla para bloquear tráfico desde el dominio
        $NFT_CMD add rule filter input ip saddr "$domain" drop
        echo "Bloqueando tráfico desde el dominio: $domain"
    fi
done < <(sqlite3 nftables_data.db "SELECT port, domain, action FROM aplicacion_bloquear;")
