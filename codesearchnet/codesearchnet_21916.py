def binpath(*paths):
    '''Like os.path.join but acts relative to this packages bin path.'''

    package_root = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(package_root, 'bin', *paths))