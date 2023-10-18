def getProcessCommandLineList(pid):
    '''
        getProcessCommandLineList - Gets the commandline (program + argumentS) of a given pid as a list.

        @param pid <int> - Process ID

        @return - None if process not found or can't be determined. Otherwise a list representing argv. First argument is process name, remainder are arguments.

        @note - Use this if you care about whether a process had a space in the commands
    '''
    try:
        with open('/proc/%d/cmdline' %(int(pid),), 'r') as f:
            cmdline = f.read()

        return cmdline.split('\x00')
    except:
        return None