def might_need_auth(f):
    """Decorate a CLI function that might require authentication.

    Catches any UnauthorizedException raised, prints a helpful message and
    then exits.
    """
    @wraps(f)
    def wrapper(cli_args):
        try:
            return_value = f(cli_args)
        except UnauthorizedException as e:
            config = config_from_env(config_from_file())
            username = _get_username(cli_args, config)

            if username is None:
                sys.exit("Please set a username (run `osf -h` for details).")
            else:
                sys.exit("You are not authorized to access this project.")

        return return_value

    return wrapper