def which(program, win_allow_cross_arch=True):
    """Identify the location of an executable file."""
    def is_exe(path):
        return os.path.isfile(path) and os.access(path, os.X_OK)

    def _get_path_list():
        return os.environ['PATH'].split(os.pathsep)

    if os.name == 'nt':
        def find_exe(program):
            root, ext = os.path.splitext(program)
            if ext:
                if is_exe(program):
                    return program
            else:
                for ext in os.environ['PATHEXT'].split(os.pathsep):
                    program_path = root + ext.lower()
                    if is_exe(program_path):
                        return program_path
            return None

        def get_path_list():
            paths = _get_path_list()
            if win_allow_cross_arch:
                alt_sys_path = os.path.expandvars(r"$WINDIR\Sysnative")
                if os.path.isdir(alt_sys_path):
                    paths.insert(0, alt_sys_path)
                else:
                    alt_sys_path = os.path.expandvars(r"$WINDIR\SysWOW64")
                    if os.path.isdir(alt_sys_path):
                        paths.append(alt_sys_path)
            return paths

    else:
        def find_exe(program):
            return program if is_exe(program) else None

        get_path_list = _get_path_list

    if os.path.split(program)[0]:
        program_path = find_exe(program)
        if program_path:
            return program_path
    else:
        for path in get_path_list():
            program_path = find_exe(os.path.join(path, program))
            if program_path:
                return program_path
    return None