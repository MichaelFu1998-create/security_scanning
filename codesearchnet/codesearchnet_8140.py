def report(function, *args, **kwds):
    """Run a function, catch, report and discard exceptions"""
    try:
        function(*args, **kwds)
    except Exception:
        traceback.print_exc()