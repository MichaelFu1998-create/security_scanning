def find_x(path1):
    '''Return true if substring is in string for files
    in specified path'''
    libs = os.listdir(path1)
    for lib_dir in libs:
        if "doublefann" in lib_dir:
            return True