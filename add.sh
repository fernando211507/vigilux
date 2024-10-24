#!/bin/bash

# Ruta al comando nft
NFT_CMD="/usr/sbin/nft"

# Conexión a la base de datos SQLite y obtención de valores
sqlite3 nftables_data.db "SELECT port, domain FROM aplicacion_permitir;" |
while IFS='|' read -r port domain; do
    # Lógica para crear reglas en nftables
    if [ "$port" != "" ]; then
        # Crear regla para permitir tráfico en el puerto
        $NFT_CMD add rule filter input tcp dport "$port" accept
        echo "Permitiendo tráfico en el puerto: $port"
    fi

    if [ "$domain" != "" ]; then
        # Crear regla para permitir tráfico desde el dominio
        $NFT_CMD add rule filter input ip saddr "$domain" accept
        echo "Permitiendo tráfico desde el dominio: $domain"
    fi
done
