def _tempfile(filename):
    """
    Create a NamedTemporaryFile instance to be passed to atomic_writer
    """
    return tempfile.NamedTemporaryFile(mode='w',
                                       dir=os.path.dirname(filename),
                                       prefix=os.path.basename(filename),
                                       suffix=os.fsencode('.tmp'),
                                       delete=False)