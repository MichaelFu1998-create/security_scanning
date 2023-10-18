def getProcessOwner(pid):
    '''
        getProcessOwner - Get the process owner of a pid

        @param pid <int> - process id

        @return - None if process not found or can't be determined. Otherwise, a dict: 
            {
                uid  - Owner UID
                name - Owner name, or None if one cannot be determined
            }
    '''
    try:
        ownerUid = os.stat('/proc/' + str(pid)).st_uid
    except:
        return None
    
    try:
        ownerName = pwd.getpwuid(ownerUid).pw_name
    except:
        ownerName = None

    return {
        'uid' : ownerUid,
        'name' : ownerName
    }