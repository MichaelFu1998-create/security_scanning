def trun_to_file(trun, fpath=None):
    """Dump the given trun to file"""

    if fpath is None:
        fpath = yml_fpath(trun["conf"]["OUTPUT"])

    with open(fpath, 'w') as yml_file:
        data = yaml.dump(trun, explicit_start=True, default_flow_style=False)
        yml_file.write(data)