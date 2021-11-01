import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


if __name__ == '__main__':
    packages = ['PySimpleGui', 'mysql-connector']

    for c in packages:
        install(c)

    

