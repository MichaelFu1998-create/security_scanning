def check_mdrun_success(logfile):
    """Check if ``mdrun`` finished successfully.

    Analyses the output from ``mdrun`` in *logfile*. Right now we are
    simply looking for the line "Finished mdrun on node" in the last 1kb of
    the file. (The file must be seeakable.)

    :Arguments:
      *logfile* : filename
         Logfile produced by ``mdrun``.

    :Returns: ``True`` if all ok, ``False`` if not finished, and
              ``None`` if the *logfile* cannot be opened
    """
    if not os.path.exists(logfile):
        return None
    with open(logfile, 'rb') as log:
        log.seek(-1024, 2)
        for line in log:
            line = line.decode('ASCII')
            if line.startswith("Finished mdrun on"):
                return True
    return False