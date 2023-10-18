def _remote_setup_engine(engine_id, nengines):
    """(Executed on remote engine) creates an ObjectEngine instance """
    if distob.engine is None:
        distob.engine = distob.ObjectEngine(engine_id, nengines)
    # TODO these imports should be unnecessary with improved deserialization
    import numpy as np
    from scipy import stats
    # TODO Using @ipyparallel.interactive still did not import to __main__
    #      so will do it this way for now.
    import __main__
    __main__.__dict__['np'] = np
    __main__.__dict__['stats'] = stats