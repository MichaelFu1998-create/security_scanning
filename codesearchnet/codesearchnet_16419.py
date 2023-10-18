def find_fann():
    '''Find doublefann library'''
    # FANN possible libs directories (as $LD_LIBRARY_PATH), also includes
    # pkgsrc framework support.
    if sys.platform == "win32":
        dirs = sys.path
        for ver in dirs:
            if os.path.isdir(ver):
                if find_x(ver):
                    return True
        raise Exception("Couldn't find FANN source libs!")
    else:
        dirs = ['/lib', '/usr/lib', '/usr/lib64', '/usr/local/lib', '/usr/pkg/lib']
        for path in dirs:
            if os.path.isdir(path):
                if find_x(path):
                    return True
        raise Exception("Couldn't find FANN source libs!")