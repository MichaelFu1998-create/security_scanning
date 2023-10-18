def scanProcessForOpenFile(pid, searchPortion, isExactMatch=True, ignoreCase=False):
    '''
        scanProcessForOpenFile - Scans open FDs for a given pid to see if any are the provided searchPortion

            @param searchPortion <str> - Filename to check
            @param isExactMatch <bool> Default True - If match should be exact, otherwise a partial match is performed.
            @param ignoreCase <bool> Default False - If True, search will be performed case-insensitively

        @return -  If result is found, the following dict is returned. If no match found on the given pid, or the pid is not found running, None is returned.
                {
                    'searchPortion' : The search portion provided
                    'pid'           : The passed pid (as an integer)
                    'owner'         : String of process owner, or "unknown" if one could not be determined
                    'cmdline'       : Commandline string
                    'fds'           : List of file descriptors assigned to this file (could be mapped several times)
                    'filenames'     : List of the filenames matched
                }
    '''
    try:
        try:
            pid = int(pid)
        except ValueError as e:
            sys.stderr.write('Expected an integer, got %s for pid.\n' %(str(type(pid)),))
            raise e

        prefixDir = "/proc/%d/fd" % (pid,)

        processFDs = os.listdir(prefixDir)

        matchedFDs = []
        matchedFilenames = []

        if isExactMatch is True:

            if ignoreCase is False:
                isMatch = lambda searchFor, totalPath : bool(searchFor == totalPath)
            else:
                isMatch = lambda searchFor, totalPath : bool(searchFor.lower() == totalPath.lower())
        else:
            if ignoreCase is False:
                isMatch = lambda searchFor, totalPath : bool(searchFor in totalPath)
            else:
                isMatch = lambda searchFor, totalPath : bool(searchFor.lower() in totalPath.lower())
            

        for fd in processFDs:
            fdPath = os.readlink(prefixDir + '/' + fd)

            if isMatch(searchPortion, fdPath):
                matchedFDs.append(fd)
                matchedFilenames.append(fdPath)


        if len(matchedFDs) == 0:
            return None

        cmdline = getProcessCommandLineStr(pid)
        owner   = getProcessOwnerStr(pid)
            
        return {
            'searchPortion' : searchPortion,
            'pid'           : pid,
            'owner'         : owner,
            'cmdline'       : cmdline,
            'fds'           : matchedFDs,
            'filenames'     : matchedFilenames, 
        }



    except OSError:
        return None
    except IOError:
        return None
    except FileNotFoundError:
        return None
    except PermissionError:
        return None