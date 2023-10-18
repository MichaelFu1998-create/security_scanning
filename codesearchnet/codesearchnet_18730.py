def exit(mod_name=""):
    """A stand-in for the normal sys.exit()

    all the magic happens here, when this is called at the end of a script it will
    figure out all the available commands and arguments that can be passed in,
    then handle exiting the script and returning the status code. 

    :Example:

        from captain import exit
        exit(__name__)

    This also acts as a guard against the script being traditionally imported, so
    even if you have this at the end of the script, it won't actually exit if the
    script is traditionally imported
    """
    if mod_name and mod_name == "__main__":
        calling_mod = sys.modules.get("__main__", None)

    else:
        calling_mod = discover_if_calling_mod()

    if calling_mod:
        s = Script(inspect.getfile(calling_mod), module=calling_mod)
        raw_args = sys.argv[1:]
        try:
            ret_code = s.run(raw_args)

        except Stop as e:
            ret_code = e.code
            msg = str(e)
            if msg:
                if ret_code != 0:
                    echo.err(msg)
                else:
                    echo.out(msg)

        sys.exit(ret_code)