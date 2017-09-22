from pkg_resources import resource_filename


def data_path(filename):
    path = resource_filename("lspcreport.tests._data", filename)
    return path