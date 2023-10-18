def lock_file(filename):
    """Locks the file by writing a '.lock' file.
       Returns True when the file is locked and
       False when the file was locked already"""

    lockfile = "%s.lock"%filename
    if isfile(lockfile):
        return False
    else:
        with open(lockfile, "w"):
            pass
    return True