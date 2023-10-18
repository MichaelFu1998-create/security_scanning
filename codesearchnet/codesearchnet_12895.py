def paramsinfo(param="", short=False):
    """ This is the human readable version of the paramsinfo() function.
        You give it a param and it prints to stdout.
    """
    if short:
        desc = 1
    else:
        desc = 0

    if param == "*":
        for key in pinfo:
            print(pinfo[str(key)][desc])
    elif param:
        try:
            print(pinfo[str(param)][desc])
        except (KeyError, ValueError) as err:
            ## TODO: paramsinfo get description by param string not working.
            ## It would be cool to have an assembly object bcz then you could
            ## just do this:
            ##
            ## print(pinfo[data.paramsinfo.keys().index(param)])
            print("\tKey name/number not recognized", err)
            raise
    else:
        print("Enter a name or number for explanation of the parameter\n")
        for key in pinfo:
            print(pinfo[str(key)][desc].split("\n")[1][2:-10])