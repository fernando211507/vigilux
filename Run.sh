#!/bin/bash

# Ruta al script shell y Python
ruta_script_shell="/var/www/html/myproject_backup/flus.sh"
ruta_script_python="/var/www/html/myproject_backup/custom_manage.py"

bash $ruta_script_shell

python3 $ruta_script_python

