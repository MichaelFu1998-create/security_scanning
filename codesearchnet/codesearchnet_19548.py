def getProcessCommandLineStr(pid):
    '''
        getProcessCommandLineStr - Gets a the commandline (program + arguments) of a given pid

        @param pid <int> - Process ID

        @return - None if process not found or can't be determined. Otherwise a string of commandline.

        @note Caution, args may have spaces in them, and you cannot surmise from this method. If you care (like trying to replay a command), use getProcessCommandLineList instead
    '''
    try:
        with open('/proc/%d/cmdline' %(int(pid),), 'r') as f:
            cmdline = f.read()
        return cmdline.replace('\x00', ' ')
    except:
        return None