packages = ['PySimpleGui', 'mysql-connector']

# implement pip as a subprocess:
import subprocess
import sys

def install(name):
    subprocess.call(['pip', 'install', name])

for c in packages:
    install(c)
