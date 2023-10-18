def indir(path):
    """
    Context manager for switching the current path of the process. Can be used:

        with indir('/tmp'):
            <do something in tmp>
    """
    cwd = os.getcwd()

    try:
        os.chdir(path)
        yield
    except Exception as e:
        raise
    finally:
        os.chdir(cwd)