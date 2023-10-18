def paraminfo(param="", short=False):
    """ Returns detailed information for the numbered parameter. 
        Further information is available in the tutorial.
        Unlike params() this function doesn't deal well with *
        It only takes one parameter at a time and returns the desc
    """

    ## If the short flag is set return the short description, otherwise
    ## return the long.
    if short:
        desc = 1
    else:
        desc = 0

    try: 
        description = pinfo[str(param)][desc]
    except (KeyError, ValueError) as err:
        ## TODO: paramsinfo get description by param string not working.
        ## It would be cool to have an assembly object bcz then you could
        ## just do this:
        ##
        ## print(pinfo[data.paramsinfo.keys().index(param)])
        print("\tKey name/number not recognized - ".format(param), err)
        raise

    return description