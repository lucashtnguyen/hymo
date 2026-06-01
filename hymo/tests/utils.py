from importlib.resources import files

def data_path(filename):
    return str(files("hymo.tests._data") / filename)
