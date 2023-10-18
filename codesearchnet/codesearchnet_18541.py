def get_variable(relpath, keyword='__version__'):
    """Read __version__ or other properties from a python file without importing it 
    
    from gist.github.com/technonik/406623 but with added keyward kwarg """
    for line in open(os.path.join(os.path.dirname(__file__), relpath), encoding='cp437'):
        if keyword in line:
            if '"' in line:
                return line.split('"')[1]
            elif "'" in line:
                return line.split("'")[1]