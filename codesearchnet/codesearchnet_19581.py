def readtxt(filepath):
    """ read file as is"""
    with open(filepath, 'rt') as f:
        lines = f.readlines()
    return ''.join(lines)