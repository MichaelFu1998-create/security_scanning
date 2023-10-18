def get_command_names():
    """
    Returns a list of command names supported
    """
    ret = []
    for f in os.listdir(COMMAND_MODULE_PATH):
        if os.path.isfile(os.path.join(COMMAND_MODULE_PATH, f)) and f.endswith(COMMAND_MODULE_SUFFIX):
            ret.append(f[:-len(COMMAND_MODULE_SUFFIX)])
    return ret