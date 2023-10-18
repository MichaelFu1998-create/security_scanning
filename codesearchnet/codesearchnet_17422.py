def callAfter(func, *args, **kwargs):
    """call a function on the main thread (async)"""
    pool = NSAutoreleasePool.alloc().init()
    obj = PyObjCAppHelperCaller_wrap.alloc().initWithArgs_((func, args, kwargs))
    obj.callAfter_(None)
    del obj
    del pool