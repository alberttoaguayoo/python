#!/usr/bin/env python3


from argparse import ArgumentParser
import subprocess
import time


def parseArguments():
	parser = ArgumentParser()
	parser.add_argument("--client", "-c",
						type=str,
						help="Define client name.")
	parser.add_argument("--external", "-e",
						type=str,
						help="External ip address.")
	parser.add_argument("--address", "-a",
						type=str,
						help="Barman ip address.")
	parser.add_argument("--port", "-p",
						type=str,
						help="cluster port.")
	return parser.parse_known_args()

def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
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
print(args)
print("instalando barman")
time.sleep(5)
subprocess.Popen('apt-get install -y barman', shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")


path="/etc/postgresql/14/test/conf.d/pruebafile.conf"

#variable para versiones mayores a postgres 9.6
deployv_conf='''max_wal_senders = 4
max_replication_slots = 4
archive_mode = on
wal_level = replica
listen_addresses = '...,DIRECCIONIP'
archive_command = 'rsync -e "ssh -p {ssh_port}" -a %p barman@{barman_ip}:/path/to/barman/home/{customer_id}/incoming/%f'
'''
print("configurando el archivo 00-deplyv.conf")
time.sleep(3)

append_new_line( path, deployv_conf)

print("done")

time.sleep(3)

pathpg= "/etc/postgresql/14/test/file.conf"

pg_hba='''host all barman {barman_ip}/32 md5
host replication streaming_barman {barman_ip}/32 md5'''

append_new_line( pathpg, pg_hba)