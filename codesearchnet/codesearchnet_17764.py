def find_files(pattern, path=None,match_name=False):
    '''
    https://stackoverflow.com/questions/1724693/find-a-file-in-python

    WARNING: pattern is by default matched to entire path not to file names
    '''
    if not path:
        path = os.getcwd()
    result = []
    for root, __, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name if match_name else os.path.join(root,name),pattern):
                result.append(os.path.join(root, name))
    return result