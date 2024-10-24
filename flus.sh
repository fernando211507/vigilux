#!/bin/sh

# Ruta al comando nft
NFT_CMD="/usr/sbin/nft"

# Eliminar todas las reglas existentes en la tabla filter
$NFT_CMD flush table filter

# Crear la tabla filter si no existe
$NFT_CMD add table filter

# Verificar y crear la cadena input si no existe
if ! $NFT_CMD list chain filter input > /dev/null 2>&1; then
    $NFT_CMD add chain filter input { type filter hook input priority 0 \; }
fi

# Verificar y crear la cadena output si no existe
if ! $NFT_CMD list chain filter output > /dev/null 2>&1; then
    $NFT_CMD add chain filter output { type filter hook output priority 0 \; }
fi

# Verificar y crear la cadena forward si no existe
if ! $NFT_CMD list chain filter forward > /dev/null 2>&1; then
    $NFT_CMD add chain filter forward { type filter hook forward priority 0 \; }
fi

echo "Reglas nftables actualizadas con éxito"
