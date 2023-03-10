#!/usr/bin/env python3

from argparse import ArgumentParser
import subprocess
import time
import sys


def parseArguments():
	parser = ArgumentParser()
	parser.add_argument("--client", "-c",
						type=str,
						help="Define client name")
	parser.add_argument("--route", "-r",
						type=str,
						help="Define absolute path")
	parser.add_argument("--external", "-e",
						type=str,
						help="External ip address.")
	parser.add_argument("--address", "-a",
						type=str,
						help="Barman ip address.")
	parser.add_argument("--port", "-p",
						type=str,
						help="cluster port.")
	return parser.parse_args()

def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name,"a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

args=parseArguments()

#Instalacion de barman
print("instalando barman")
time.sleep(1)
subprocess.Popen('apt-get install -y barman', shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")

#CONFIGURACION DEL ARCHIVO 00-DEPLOYV.CONF

subprocess.Popen('mkdir {route}/conf.d'.format(route=args.route) , shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")


#variable para versiones mayores a postgres 9.6
path_deployv=args.route + "conf.d/00-deployv.conf"
deployv_conf='''max_wal_senders = 4
max_replication_slots = 4
archive_mode = on
wal_level = replica
listen_addresses = '...,{external_ip}'
archive_command = 'rsync -e "ssh -p {ssh_port}" -a %p barman@{barman_ip}:/path/to/barman/home/{customer_id}/incoming/%f'
'''.format(external_ip=args.external, ssh_port=args.port, barman_ip=args.address, customer_id=args.client)

print("configurando el archivo 00-deplyv.conf")
time.sleep(2)

append_new_line(path_deployv, deployv_conf)

print("archivo configurado")

time.sleep(3)

#CONFIGURACION DEL ARCHIVO PG_HBA.CONF

path_postgres=args.route + "pg_hba.conf"

pg_hba='''host all barman {barman_ip}/32 md5
host replication streaming_barman {barman_ip}/32 md5
'''.format(barman_ip=args.address)

append_new_line(path_postgres , pg_hba)

#Agregando reglas de firewall

subprocess.Popen('ufw allow from {barman_ip} to any port {cluster_port}'.format(barman_ip=args.address , cluster_port=args.port) , shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")

subprocess.Popen('sudo iptables -I INPUT 1 -p tcp --dport {cluster_port} -i eth0 ! -s {barman_ip} -j DROP'.format(cluster_port=args.port , barman_ip=args.external), shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")

print("reglas de firewall agregadas")
time.sleep(2)

# creando los usuarios Barman

print("crear usuarios postgres")
time.sleep(2)
subprocess.Popen("psql -c \"create user barman with superuser password \'barman_password\';\"", shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")
subprocess.Popen("psql -c \"create user streaming_barman with REPLICATION password \'streaming_password\'\";", shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")
print("Usuarios creados")

#Creando archivo de configuracion Barman

subprocess.Popen('mkdir /etc/barman.d/', shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")
subprocess.Popen('touch /etc/barman.d/{customer_id}.conf'.format(customer_id=args.client), shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")

	
path_barman="/etc/barman.d/" + args.client + ".conf"

barman_conf='''
[{customer_id}]
description =  "A brief description"
conninfo = host={postgres_ip} user=barman dbname=postgres port={cluster_port} password=barman_password
backup_method = postgres
streaming_conninfo = host={postgres_ip} user=streaming_barman dbname=postgres port={cluster_port} password=streaming_password
streaming_archiver = on
slot_name = barman_{customer_id}
archiver=on
'''.format(customer_id=args.client , postgres_ip=args.external , cluster_port=args.port)

append_new_line(path_barman , barman_conf)

time.sleep(2)
print("Configuracion exitosa")

#subprocess.Popen(''' barman receive-wal --create-slot {customer_id}
#barman switch-xlog --force {customer_id}
#barman switch-xlog --force --archive {customer_id}
#barman backup {customer_id}'''.format(customer_id=args.client), shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")

sys.exit()