def getProcessOwnerStr(pid):
    '''
        getProcessOwner - Get Process owner of a pid as a string instead of components (#getProcessOwner)

        @return - Returns username if it can be determined, otherwise uid, otherwise "unknown"
    '''
    ownerInfo = getProcessOwner(pid)
    if ownerInfo:
        if ownerInfo['name']:
            owner = ownerInfo['name']
        else:
            owner = str(ownerInfo['uid'])
    else:
        owner = 'unknown'

    return owner