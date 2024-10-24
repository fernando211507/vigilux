import sqlite3
import subprocess


# Conexión a la base de datos SQLite
conn = sqlite3.connect('nftables_data.db')
cursor = conn.cursor()

# Obtener valores de la base de datos
cursor.execute("SELECT port, domain FROM aplicacion_permitir")
rows = cursor.fetchall()

# Comandos nftables para permitir tráfico en puertos y dominios
for row in rows:
    port, domain = row
    if port:
        # Crear regla para permitir tráfico en el puerto
        subprocess.run(["/usr/sbin/nft", "add", "rule", "filter", "input", "tcp", "dport", str(port), "accept"])
        print(f"Permitiendo tráfico en el puerto: {port}")

    if domain:
        # Crear regla para permitir tráfico desde el dominio
        subprocess.run(["/usr/sbin/nft", "add", "rule", "filter", "input", "ip", "saddr", str(domain), "accept"])
        print(f"Permitiendo tráfico desde el dominio: {domain}")

# Cerrar conexión a la base de datos
conn.close()

import sqlite3
import subprocess

# Conexión a la base de datos para bloquear tráfico
conn_block = sqlite3.connect('nftables_data.db')
cursor_block = conn_block.cursor()

# Obtener valores de la base de datos para bloquear tráfico
cursor_block.execute("SELECT port, domain FROM aplicacion_bloquear")
rows_block = cursor_block.fetchall()

for row in rows_block:
    port, domain = row
    if port:
        subprocess.run(["/usr/sbin/nft", "add", "rule", "filter", "input", "tcp", "dport", str(port), "drop"])
        print(f"Bloqueando tráfico en puerto: {port}")
    if domain:
        subprocess.run(["/usr/sbin/nft", "add", "rule", "filter", "input", "ip", "saddr", str(domain), "drop"])
        print(f"Bloqueando tráfico desde dominio: {domain}")

conn_block.close()
