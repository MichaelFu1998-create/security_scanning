def scanAllProcessesForMapping(searchPortion, isExactMatch=False, ignoreCase=False):
    '''
        scanAllProcessesForMapping - Scans all processes on the system for a given search pattern.

            @param searchPortion <str> - A mapping for which to search, example: libc or python or libz.so.1. Give empty string to return all mappings.
            @param isExactMatch <bool> Default False - If match should be exact, otherwise a partial match is performed.
            @param ignoreCase <bool> Default False - If True, search will be performed case-insensitively

        @return - <dict> - A dictionary of pid -> mappingResults for each pid that matched the search pattern. For format of "mappingResults", @see scanProcessForMapping
    '''
    pids = getAllRunningPids()

    # Since processes could disappear, we run the scan as fast as possible here with a list comprehension, then assemble the return dictionary later.
    mappingResults = [scanProcessForMapping(pid, searchPortion, isExactMatch, ignoreCase) for pid in pids]
    ret = {}
    for i in range(len(pids)):
        if mappingResults[i] is not None:
            ret[pids[i]] = mappingResults[i]

    return ret