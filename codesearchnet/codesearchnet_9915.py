def service_start(service=None, param=None):
    """
        Launch a Process, return his pid
    """
    if service is not None:
        to_run = ["python", service]
        if param is not None:
            to_run += param
        return subprocess.Popen(to_run)
    return False