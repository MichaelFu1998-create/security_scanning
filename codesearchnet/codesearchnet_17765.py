def find_directories(pattern, path=None,match_name=False):
    '''
    WARNING: pattern is matched to entire path, not directory names, unless
    match_name = True
    '''
    if not path:
        path = os.getcwd()
    result = []
    for root, __, __ in os.walk(path):
        match_against = os.path.basename(root) if match_name else root
        try:
            does_match = pattern.match(match_against)
        except AttributeError:
            does_match = fnmatch.fnmatch(match_against,pattern)
        if does_match:
            result.append(root)
    return result