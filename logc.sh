#!/bin/bash

#Ruta al archivo de logs
LOG_FILE="/var/log/suricata/suricata.log"

#verifica si existe el archivo de log
if [ ! -f "$LOG_FILE" ]; then
	echo "el archivo de log no existe."
	exit 1
fi

#extraer registros especificos del archivo log
pings=$(grep "Pin detectado" "LOG_FILE" | sed "s/'//g")

#crear un archivo temporal para insertar los datos
tm_file=$(mktemp)
echo "pings" > "$tmp_file"

#iterar sobre los registros y realizar la inserccion en la base de datos
while IFS= read -r linea; do
	sqlite3 nftables_data.db "INSERT INTO aplicacion_ping (registro) VALUES ('$linea');"
	if [ $? -ne 0 ]; then
	   echo "Error al insertar en la base de datos."
	   rm "$tmp_file"
	   exit 1
	fi
done < "$tmp_file"
#eliminar el archivo temporal
rm "$tmp_file"

echo "Registro de pings insertados en la base de datos"
