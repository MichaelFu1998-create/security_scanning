def find_executable_files():
    """
    Find max 5 executables that are responsible for this repo.
    """
    files = glob.glob("*") + glob.glob("*/*") + glob.glob('*/*/*')
    files = filter(lambda f: os.path.isfile(f), files)
    executable = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
    final = []
    for filename in files:
        if os.path.isfile(filename):
            st = os.stat(filename)
            mode = st.st_mode
            if mode & executable:
                final.append(filename)
                if len(final) > 5:
                    break
    return final