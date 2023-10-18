def cmd():
    '''Return a command to launch a subshell'''

    if platform == 'win':
        return ['cmd.exe', '/K']

    elif platform == 'linux':
        ppid = os.getppid()
        ppid_cmdline_file = '/proc/{0}/cmdline'.format(ppid)
        try:
            with open(ppid_cmdline_file) as f:
                cmd = f.read()
            if cmd.endswith('\x00'):
                cmd = cmd[:-1]
            cmd = cmd.split('\x00')
            return cmd + [binpath('subshell.sh')]
        except:
            cmd = 'bash'

    else:
        cmd = 'bash'

    return [cmd, binpath('subshell.sh')]