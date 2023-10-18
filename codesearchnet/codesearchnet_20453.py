def lesspager(lines):
    """
    Use for streaming writes to a less process
    Taken from pydoc.pipepager:
    /usr/lib/python2.7/pydoc.py
    and
    /usr/lib/python3.5/pydoc.py
    """
    cmd = "less -S"
    if sys.version_info[0] >= 3:
        """Page through text by feeding it to another program."""
        import subprocess
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
        try:
            with io.TextIOWrapper(proc.stdin, errors='backslashreplace') as pipe:
                try:
                    for l in lines:
                        pipe.write(l)
                except KeyboardInterrupt:
                    # We've hereby abandoned whatever text hasn't been written,
                    # but the pager is still in control of the terminal.
                    pass
        except OSError:
            pass # Ignore broken pipes caused by quitting the pager program.
        while True:
            try:
                proc.wait()
                break
            except KeyboardInterrupt:
                # Ignore ctl-c like the pager itself does.  Otherwise the pager is
                # left running and the terminal is in raw mode and unusable.
                pass

    else:
        proc = os.popen(cmd, 'w')
        try:
            for l in lines:
                proc.write(l)
        except IOError:
            proc.close()
            sys.exit()