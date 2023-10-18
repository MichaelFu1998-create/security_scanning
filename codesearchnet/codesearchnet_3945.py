def _win32_dir(path, star=''):
    """
    Using the windows cmd shell to get information about a directory
    """
    from ubelt import util_cmd
    import re
    wrapper = 'cmd /S /C "{}"'  # the /S will preserve all inner quotes
    command = 'dir /-C "{}"{}'.format(path, star)
    wrapped = wrapper.format(command)
    info = util_cmd.cmd(wrapped, shell=True)
    if info['ret'] != 0:
        from ubelt import util_format
        print('Failed command:')
        print(info['command'])
        print(util_format.repr2(info, nl=1))
        raise OSError(str(info))
    # parse the output of dir to get some info
    # Remove header and footer
    lines = info['out'].split('\n')[5:-3]
    splitter = re.compile('( +)')
    for line in lines:
        parts = splitter.split(line)
        date, sep, time, sep, ampm, sep, type_or_size, sep = parts[:8]
        name = ''.join(parts[8:])
        # if type is a junction then name will also contain the linked loc
        if name == '.' or name == '..':
            continue
        if type_or_size in ['<JUNCTION>', '<SYMLINKD>', '<SYMLINK>']:
            # colons cannot be in path names, so use that to find where
            # the name ends
            pos = name.find(':')
            bpos = name[:pos].rfind('[')
            name = name[:bpos - 1]
            pointed = name[bpos + 1:-1]
            yield type_or_size, name, pointed
        else:
            yield type_or_size, name, None