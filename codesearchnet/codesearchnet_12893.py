def paramname(param=""):
    """ Get the param name from the dict index value.
    """

    try: 
        name = pinfo[str(param)][0].strip().split(" ")[1]
    except (KeyError, ValueError) as err:
        ## TODO: paramsinfo get description by param string not working.
        ## It would be cool to have an assembly object bcz then you could
        ## just do this:
        ##
        ## print(pinfo[data.paramsinfo.keys().index(param)])
        print("\tKey name/number not recognized - ".format(param), err)
        raise

    return name