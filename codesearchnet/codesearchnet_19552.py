def scanProcessForMapping(pid, searchPortion, isExactMatch=False, ignoreCase=False):
    '''
        scanProcessForMapping - Searches a given pid's mappings for a certain pattern.

            @param pid <int> - A running process ID on this system
            @param searchPortion <str> - A mapping for which to search, example: libc or python or libz.so.1. Give empty string to return all mappings.
            @param isExactMatch <bool> Default False - If match should be exact, otherwise a partial match is performed.
            @param ignoreCase <bool> Default False - If True, search will be performed case-insensitively

            @return <dict> - If result is found, the following dict is returned. If no match found on the given pid, or pid is not found running, None is returned.
                {
                    'searchPortion' : The passed search pattern
                    'pid'           : The passed pid (as an integer)
                    'owner'         : String of process owner, or uid if no mapping can be found, or "unknown" if neither could be determined.
                    'cmdline'       : Commandline string
                    'matchedMappings' : All mappings likes that matched the given search pattern
                }

    '''
    try:   
        try:
            pid = int(pid)
        except ValueError as e:
            sys.stderr.write('Expected an integer, got %s for pid.\n' %(str(type(pid)),))
            raise e
            
        with open('/proc/%d/maps' %(pid,), 'r') as f:
            contents = f.read()

        lines = contents.split('\n')
        matchedMappings = []
    
        if isExactMatch is True:

            if ignoreCase is False:
                isMatch = lambda searchFor, searchIn : bool(searchFor == searchIn)
            else:
                isMatch = lambda searchFor, searchIn : bool(searchFor.lower() == searchIn.lower())
        else:
            if ignoreCase is False:
                isMatch = lambda searchFor, searchIn : bool(searchFor in searchIn)
            else:
                isMatch = lambda searchFor, searchIn : bool(searchFor.lower() in searchIn.lower())
                

        for line in lines:
            portion = ' '.join(line.split(' ')[5:]).lstrip()
            if isMatch(searchPortion, portion):
                matchedMappings.append('\t' + line)

        if len(matchedMappings) == 0:
            return None


        cmdline = getProcessCommandLineStr(pid)
        owner   = getProcessOwnerStr(pid)

        return {
            'searchPortion' : searchPortion,
            'pid'           : pid,
            'owner'         : owner,
            'cmdline'       : cmdline,
            'matchedMappings' : matchedMappings,
        }
    except OSError:
        return None
    except IOError:
        return None
    except FileNotFoundError:
        return None
    except PermissionError:
        return None