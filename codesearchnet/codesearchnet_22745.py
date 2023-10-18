def _CallWindowsNetCommand(parameters):
    '''
    Call Windows NET command, used to acquire/configure network services settings.

    :param parameters: list of command line parameters

    :return: command output
    '''
    import subprocess
    popen = subprocess.Popen(["net"] + parameters, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdoutdata, stderrdata = popen.communicate()
    if stderrdata:
        raise OSError("Failed on call net.exe: %s" % stderrdata)
    return stdoutdata