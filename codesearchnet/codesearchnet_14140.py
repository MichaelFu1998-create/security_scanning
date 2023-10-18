def vw_envs(filter=None):
    """
    :return: python environments in ~/.virtualenvs

    :param filter: if this returns False the venv will be ignored

    >>> vw_envs(filter=venv_has_script('pip'))
    """
    vw_root=os.path.abspath(os.path.expanduser(os.path.expandvars('~/.virtualenvs')))
    venvs=[]
    for directory in os.listdir(vw_root):
        venv=os.path.join(vw_root, directory)
        if os.path.isdir(os.path.join(venv)):
            if filter and not filter(venv):
                continue
            venvs.append(venv)
    return sorted(venvs)