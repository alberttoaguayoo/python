#!/usr/bin/env python3


from argparse import ArgumentParser
import subprocess
import time

#pedir el path en vez del nombre del cliente

def parseArguments():
	parser = ArgumentParser()
	parser.add_argument("--client", "-c",
						type=str,
						help="Define client name")
	parser.add_argument("--route", "-r",
						type=str,
						help="Define route.")
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
    with open(file_name,"/conf.d/00-deployv.conf" ,"a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

'''
texto que se tiene que agregar al archivo de 00-deployv.conf
max_wal_senders = 4
max_replication_slots = 4
archive_mode = on                       # Solo si la versión de postgres es }= 9.6
hot_standby = on                        # Solo si la versión es menor a 9.6
wal_level = replica                     # Solo si la versión de postgres es }= 9.6
wal_level = hot_standby                 # Solo si la versión es menor a 9.6
listen_addresses = '...,{external_ip}'  # Se debe agregar la IP externa del server sumada a las que ya se encuentren configuradas.
archive_command = 'rsync -e "ssh -p {ssh_port}" -a %p barman@{barman_ip}:/path/to/barman/home/{customer_id}/incoming/%f'
'''

args=parseArguments()

print("instalando barman")
time.sleep(1)
#subprocess.Popen('apt-get install -y barman', shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")


#CONFIGURACION DEL ARCHIVO 00-DEPLOYV.CONF

#variable para versiones mayores a postgres 9.6
deployv_conf='''max_wal_senders = 4
max_replication_slots = 4
archive_mode = on
wal_level = replica
listen_addresses = '...,{external_ip}'
archive_command = 'rsync -e "ssh -p {ssh_port}" -a %p barman@{barman_ip}:/path/to/barman/home/{customer_id}/incoming/%f'
'''.format(external_ip=args.external, ssh_port=args.port, barman_ip=args.address, customer_id=args.client)

print("configurando el archivo 00-deplyv.conf")
time.sleep(3)

append_new_line( args.route, deployv_conf)

print("archivo configurado")

time.sleep(3)

#CONFIGURACION DEL ARCHIVO PG_HBA.CONF

pathpg= "/etc/postgresql/14/test/file.conf"

pg_hba='''host all barman {barman_ip}/32 md5
host replication streaming_barman {barman_ip}/32 md5'''

append_new_line( pathpg, pg_hba)