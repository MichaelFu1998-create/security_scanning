def venv_has_script(script):
    """
    :param script: script to look for in bin folder
    """
    def f(venv):
        path=os.path.join(venv, 'bin', script)
        if os.path.isfile(path):
            return True
    return f