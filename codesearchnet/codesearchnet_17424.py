def stopEventLoop():
    """
    Stop the current event loop if possible
    returns True if it expects that it was successful, False otherwise
    """
    stopper = PyObjCAppHelperRunLoopStopper_wrap.currentRunLoopStopper()
    if stopper is None:
        if NSApp() is not None:
            NSApp().terminate_(None)
            return True
        return False
    NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
        0.0,
        stopper,
        'performStop:',
        None,
        False)
    return True