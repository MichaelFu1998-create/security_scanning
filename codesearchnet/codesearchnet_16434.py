def clean_outputs(fn):
    """Decorator for CLI with Sentry client handling.

    see https://github.com/getsentry/raven-python/issues/904 for more details.
    """

    @wraps(fn)
    def clean_outputs_wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except SystemExit as e:
            sys.stdout = StringIO()
            sys.exit(e.code)  # make sure we still exit with the proper code
        except Exception as e:
            sys.stdout = StringIO()
            raise e

    return clean_outputs_wrapper