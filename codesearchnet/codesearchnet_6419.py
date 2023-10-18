def get_or_guess_paths_to_mutate(paths_to_mutate):
    """
    :type paths_to_mutate: str or None
    :rtype: str
    """
    if paths_to_mutate is None:
        # Guess path with code
        this_dir = os.getcwd().split(os.sep)[-1]
        if isdir('lib'):
            return 'lib'
        elif isdir('src'):
            return 'src'
        elif isdir(this_dir):
            return this_dir
        elif isdir(this_dir.replace('-', '_')):
            return this_dir.replace('-', '_')
        elif isdir(this_dir.replace(' ', '_')):
            return this_dir.replace(' ', '_')
        elif isdir(this_dir.replace('-', '')):
            return this_dir.replace('-', '')
        elif isdir(this_dir.replace(' ', '')):
            return this_dir.replace(' ', '')
        else:
            raise FileNotFoundError(
                'Could not figure out where the code to mutate is. '
                'Please specify it on the command line using --paths-to-mutate, '
                'or by adding "paths_to_mutate=code_dir" in setup.cfg to the [mutmut] section.')
    else:
        return paths_to_mutate