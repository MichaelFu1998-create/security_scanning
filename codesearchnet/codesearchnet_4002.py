def autoset_settings(set_var):
    """Autoset GPU parameters using CUDA_VISIBLE_DEVICES variables.

    Return default config if variable not set.
    :param set_var: Variable to set. Must be of type ConfigSettings
    """
    try:
        devices = ast.literal_eval(os.environ["CUDA_VISIBLE_DEVICES"])
        if type(devices) != list and type(devices) != tuple:
            devices = [devices]
        if len(devices) != 0:
            set_var.GPU = len(devices)
            set_var.NB_JOBS = len(devices)
            warnings.warn("Detecting CUDA devices : {}".format(devices))

    except KeyError:
        set_var.GPU = check_cuda_devices()
        set_var.NB_JOBS = set_var.GPU
        warnings.warn("Detecting {} CUDA devices.".format(set_var.GPU))
        if not set_var.GPU:
            warnings.warn("No GPU automatically detected. Setting SETTINGS.GPU to 0, " +
                          "and SETTINGS.NB_JOBS to cpu_count.")
            set_var.GPU = 0
            set_var.NB_JOBS = multiprocessing.cpu_count()

    return set_var