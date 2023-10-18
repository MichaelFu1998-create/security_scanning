def set_cmd_env_var(value):
    """Decorator that sets the temple command env var to value"""
    def func_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            previous_cmd_env_var = os.getenv(temple.constants.TEMPLE_ENV_VAR)
            os.environ[temple.constants.TEMPLE_ENV_VAR] = value
            try:
                ret_val = function(*args, **kwargs)
            finally:
                if previous_cmd_env_var is None:
                    del os.environ[temple.constants.TEMPLE_ENV_VAR]
                else:
                    os.environ[temple.constants.TEMPLE_ENV_VAR] = previous_cmd_env_var

            return ret_val
        return wrapper
    return func_decorator