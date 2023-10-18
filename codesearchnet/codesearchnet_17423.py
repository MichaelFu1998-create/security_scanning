def callLater(delay, func, *args, **kwargs):
    """call a function on the main thread after a delay (async)"""
    pool = NSAutoreleasePool.alloc().init()
    obj = PyObjCAppHelperCaller_wrap.alloc().initWithArgs_((func, args, kwargs))
    obj.callLater_(delay)
    del obj
    del pool