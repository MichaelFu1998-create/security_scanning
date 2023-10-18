def ListMappedNetworkDrives():
    '''
    On Windows, returns a list of mapped network drives

    :return: tuple(string, string, bool)
        For each mapped netword drive, return 3 values tuple:
            - the local drive
            - the remote path-
            - True if the mapping is enabled (warning: not reliable)
    '''
    if sys.platform != 'win32':
        raise NotImplementedError
    drives_list = []
    netuse = _CallWindowsNetCommand(['use'])
    for line in netuse.split(EOL_STYLE_WINDOWS):
        match = re.match("(\w*)\s+(\w:)\s+(.+)", line.rstrip())
        if match:
            drives_list.append((match.group(2), match.group(3), match.group(1) == 'OK'))
    return drives_list