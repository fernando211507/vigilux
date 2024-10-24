
from django.shortcuts import render, redirect
from subprocess import Popen
from .forms import PermitirForm, BloquearForm, DNSQueryForm
from .models import Permitir, Bloquear, Ping, DNSQuery, RegistroActividad
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import JsonResponse
import subprocess
from datetime import datetime



def create_rule(request):
    if request.method == 'POST':
        form = PermitirForm(request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.save()

            # Lógica para aplicar reglas a nftablesc
            apply_nft_rule(rule)  # Llamada a función para aplicar la regla a nftables

            return redirect('rule_list') # Redirigir a la lista de reglas else:
        form = PermitirForm()
    return render(request, 'nftables_panel/agregar_regla.html', {'form': form})

def rule_list(request):
    rules = Permitir.objects.all()
    return render(request, 'nftables_panel/lista_de_reglas.html', {'rules': rules})

def apply_nft_rule(rule):
    # Lógica para aplicar la regla a nftables
    if rule.port and rule.domain and rule.action:
        # Comando para añadir la regla a nftables
        command = f"nft add rule ... -p {rule.port} -d {rule.domain} -a {rule.action}"  # Reemplaza con tu sintaxis de nftables
        subprocess.run(command, shell=True)
        # Se ejecuta el comando para agregar la regla a nftables

# agregar Bloquear para la red desde aqui
def create_rule(request):
    if request.method == 'POST':
        form = BloquearForm(request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.save()

            # Lógica para aplicar reglas a nftables
            apply_nft_rule(rule)  # Llamada a función para aplicar la regla a nftables

            return redirect('rule_list')  # Redirigir a la lista de reglas
    else:
        form = BloquearForm()
    return render(request, 'nftables_panel/agregar_regla.html', {'form': form})

def rule_list(request):
    rules = Bloquear.objects.all()
    return render(request, 'nftables_panel/lista_de_reglas.html', {'rules': rules})

def apply_nft_rule(rule):
    # Lógica para aplicar la regla a nftables
    if rule.port and rule.domain and rule.action:
        # Comando para añadir la regla a nftables
        command = f"nft add rule ... -p {rule.port} -d {rule.domain} -a {rule.action}"  # Reemplaza con tu sintaxis de nftables
        subprocess.run(command, shell=True)
        # Se ejecuta el comando para agregar la regla a nftables

def ping_list(request):
    pings = Ping.objects.all().order_by('-timestamp')
    return render(request, 'alert_template.html', {'pings': pings})

def dns_lookup(request):
    if request.method == 'POST':
        form = DNSQueryForm(request.POST)
        if form.is_valid():
            dns_query = form.save(commit=False)
            domain = dns_query.domain

            # Ejecutar nslookup para obtener la IP
            try:
                result = subprocess.run(['nslookup', domain], stdout=subprocess.PIPE, text=True)
                # Extraer la dirección IP de la salida del comando nslookup
                output = result.stdout.split('Address: ')[-1].strip()
                dns_query.ip_address = output
            except Exception as e:
                dns_query.ip_address = None  # Manejar el caso de error

            dns_query.save()
            return redirect('dns_result', pk=dns_query.pk)
    else:
        form = DNSQueryForm()
    return render(request, 'dns_lookup.html', {'form': form})

def dns_result(request, pk):
    dns_query = DNSQuery.objects.get(pk=pk)
    return render(request, 'dns_result.html', {'dns_query': dns_query})

#admin

def informes(request):
    filtro = request.GET.get('filtro', 'todos')
    
    if filtro == 'bloquear':
        registros = RegistroActividad.objects.filter(modelo_afectado='Bloquear').order_by('-fecha')
    elif filtro == 'permitir':
        registros = RegistroActividad.objects.filter(modelo_afectado='Permitir').order_by('-fecha')
    elif filtro == 'ping':
        registros = RegistroActividad.objects.filter(modelo_afectado='Ping').order_by('-fecha')
    elif filtro == 'dnsquery':
        registros = RegistroActividad.objects.filter(modelo_afectado='DNSQuery').order_by('-fecha')
    else:
        registros = RegistroActividad.objects.all().order_by('-fecha')
    

    return render(request, 'admin/informes.html', {'registros': registros, 'filtro': filtro})