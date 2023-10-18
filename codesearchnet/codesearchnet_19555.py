def scanAllProcessesForOpenFile(searchPortion, isExactMatch=True, ignoreCase=False):
    '''
        scanAllProcessessForOpenFile - Scans all processes on the system for a given filename

            @param searchPortion <str> - Filename to check
            @param isExactMatch <bool> Default True - If match should be exact, otherwise a partial match is performed.
            @param ignoreCase <bool> Default False - If True, search will be performed case-insensitively

        @return - <dict> - A dictionary of pid -> mappingResults for each pid that matched the search pattern. For format of "mappingResults", @see scanProcessForOpenFile
    '''
    pids = getAllRunningPids()

    # Since processes could disappear, we run the scan as fast as possible here with a list comprehension, then assemble the return dictionary later.
    mappingResults = [scanProcessForOpenFile(pid, searchPortion, isExactMatch, ignoreCase) for pid in pids]
    ret = {}
    for i in range(len(pids)):
        if mappingResults[i] is not None:
            ret[pids[i]] = mappingResults[i]

    return ret