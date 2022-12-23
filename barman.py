#!/usr/bin/env python3


from argparse import ArgumentParser
from subprocess import STDOUT, check_call
import os

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

args=parseArguments()
print(args)


check_call(['apt-get', 'install', '-y', 'barman'],
     stdout=open(os.devnull,'wb'), stderr=STDOUT) 