def init(log_level=ERROR):
    '''
    Enables explicit relative import in sub-modules when ran as __main__
    :param log_level: module's inner logger level (equivalent to logging pkg)
    '''
    global _initialized
    if _initialized:
        return
    else:
        _initialized = True
    # find caller's frame
    frame = currentframe()
    # go 1 frame back to find who imported us
    frame = frame.f_back
    _init(frame, log_level)