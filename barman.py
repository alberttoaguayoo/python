#!/usr/bin/env python3


from argparse import ArgumentParser

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

def package_installation(self):
    self.apt = "apt "
    self.ins = "install "
    self.packages = "barman"

    self.color.print_green("[+] Barman nstallation is starting:")

    for self.items in self.packages.split():
        self.command = str(self.apt) + str(self.ins) + str(self.items)

        subprocess.run(self.command.split())
        self.color.print_blue("\t[+] Package [{}] Installed".format(str(self.items)))