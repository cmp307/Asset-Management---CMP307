import subprocess
import sys

packages = ['PySimpleGui', 'mysql-connector', 'numpy'] #libraries to install

def install(name):
    subprocess.call(['pip', 'install', name])   #install library using pip install

for c in packages:
    install(c)
