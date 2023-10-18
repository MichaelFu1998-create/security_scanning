def decorate(msg="", waitmsg="Please wait"):
        """
        Decorated methods progress will be displayed to the user as a spinner.
        Mostly for slower functions that do some network IO.
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                spin = Spinner(msg=msg, waitmsg=waitmsg)
                spin.start()
                a = None
                try:
                    a = func(*args, **kwargs)
                except Exception as e:
                    spin.msg = "Something went wrong: "
                    spin.stop_spinning()
                    spin.join()
                    raise e
                spin.stop_spinning()
                spin.join()
                return a

            return wrapper

        return decorator