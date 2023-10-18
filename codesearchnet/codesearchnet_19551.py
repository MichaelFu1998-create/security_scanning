def scanAllProcessesForCwd(searchPortion, isExactMatch=False):
    '''
        scanAllProcessesForCwd - Scans all processes on the system for a given search pattern.

            @param searchPortion <str> - Any portion of directory to search
            @param isExactMatch <bool> Default False - If match should be exact, otherwise a partial match is performed.

        @return - <dict> - A dictionary of pid -> cwdResults for each pid that matched the search pattern. For format of "cwdResults", @see scanProcessForCwd
    '''
    
    pids = getAllRunningPids()

    cwdResults = [scanProcessForCwd(pid, searchPortion, isExactMatch) for pid in pids]
    ret = {}
    for i in range(len(pids)):
        if cwdResults[i] is not None:
            ret[pids[i]] = cwdResults[i]

    return ret