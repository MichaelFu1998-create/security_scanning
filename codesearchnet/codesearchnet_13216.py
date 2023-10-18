def deprecated(version, version_removed):
    '''This is a decorator which can be used to mark functions
    as deprecated.

    It will result in a warning being emitted when the function is used.'''

    def __wrapper(func, *args, **kwargs):
        '''Warn the user, and then proceed.'''
        code = six.get_function_code(func)
        warnings.warn_explicit(
            "{:s}.{:s}\n\tDeprecated as of JAMS version {:s}."
            "\n\tIt will be removed in JAMS version {:s}."
            .format(func.__module__, func.__name__,
                    version, version_removed),
            category=DeprecationWarning,
            filename=code.co_filename,
            lineno=code.co_firstlineno + 1
        )
        return func(*args, **kwargs)

    return decorator(__wrapper)