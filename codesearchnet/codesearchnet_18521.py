def bug_info(exc_type, exc_value, exc_trace):
    """Prints the traceback and invokes the ipython debugger on any exception

    Only invokes ipydb if you are outside ipython or python interactive session.
    So scripts must be called from OS shell in order for exceptions to ipy-shell-out.

    Dependencies:
      Needs `pip install ipdb`

    Arguments:
      exc_type (type): The exception type/class (e.g. RuntimeError)
      exc_value (Exception): The exception instance (e.g. the error message passed to the Exception constructor)
      exc_trace (Traceback): The traceback instance
    
    References:
      http://stackoverflow.com/a/242531/623735

    Example Usage:
      $  python -c 'from pug import debug;x=[];x[0]'
      Traceback (most recent call last):
        File "<string>", line 1, in <module>
      IndexError: list index out of range

      > <string>(1)<module>()

      ipdb> x
      []
      ipdb> locals()
      {'__builtins__': <module '__builtin__' (built-in)>, '__package__': None, 'x': [], 'debug': <module 'pug.debug' from 'pug/debug.py'>, '__name__': '__main__', '__doc__': None}
      ipdb> 
    """
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
        # We are in interactive mode or don't have a tty-like device, so we call the default hook
        sys.__excepthook__(exc_type, exc_value, exc_trace)
    else:
        # Need to import non-built-ins here, so if dependencies haven't been installed, both tracebacks will print
        # (e.g. the ImportError and the Exception that got you here)
        import ipdb
        # We are NOT in interactive mode, print the exception
        traceback.print_exception(exc_type, exc_value, exc_trace)
        print
        # Start the debugger in post-mortem mode.
        ipdb.post_mortem(exc_trace)