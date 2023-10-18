def scanProcessForCwd(pid, searchPortion, isExactMatch=False):
    '''
        scanProcessForCwd - Searches a given pid's cwd for a given pattern

            @param pid <int> - A running process ID on this system
            @param searchPortion <str> - Any portion of directory to search
            @param isExactMatch <bool> Default False - If match should be exact, otherwise a partial match is performed.

            @return <dict> - If result is found, the following dict is returned. If no match found on the given pid, or pid is not found running, None is returned.
                {
                    'searchPortion' : The passed search pattern
                    'pid'           : The passed pid (as an integer)
                    'owner'         : String of process owner, or uid if no mapping can be found, or "unknown" if neither could be determined.
                    'cmdline'       : Commandline string
                    'cwd'           : The exact cwd of matched process
                }
    '''
    try:   
        try:
            pid = int(pid)
        except ValueError as e:
            sys.stderr.write('Expected an integer, got %s for pid.\n' %(str(type(pid)),))
            raise e
            

        cwd = getProcessCwd(pid)
        if not cwd:
            return None

        isMatch = False
        if isExactMatch is True:
            if searchPortion == cwd:
                isMatch = True
            else:
                if searchPortion.endswith('/') and searchPortion[:-1] == cwd:
                    isMatch = True
        else:
            if searchPortion in cwd:
                isMatch = True
            else:
                if searchPortion.endswith('/') and searchPortion[:-1] in cwd:
                    isMatch = True

        if not isMatch:
            return None

        cmdline = getProcessCommandLineStr(pid)
        owner   = getProcessOwnerStr(pid)

        return {
            'searchPortion' : searchPortion,
            'pid'           : pid,
            'owner'         : owner,
            'cmdline'       : cmdline,
            'cwd'           : cwd,
        }
    except OSError:
        return None
    except IOError:
        return None
    except FileNotFoundError:
        return None
    except PermissionError:
        return None