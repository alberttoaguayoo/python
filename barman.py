from argparse import ArgumentParser

def parseArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("--client", "-c",
						type=str,
						help="Define client name.")
	parser.add_argument("--external", "-e",
						type=str,
						help="External ip address.")
	return parser.parse_known_args()


'''
* Postgres cluster name.
* External ip
* Barman ip
* Port
* Customer id
'''