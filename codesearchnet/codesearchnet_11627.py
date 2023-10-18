def _truthyConfValue(v):
    ''' Determine yotta-config truthiness. In yotta config land truthiness is
        different to python or json truthiness (in order to map nicely only
        preprocessor and CMake definediness):

          json      -> python -> truthy/falsey
          false     -> False  -> Falsey
          null      -> None   -> Falsey
          undefined -> None   -> Falsey
          0         -> 0      -> Falsey
          ""        -> ""     -> Truthy (different from python)
          "0"       -> "0"    -> Truthy
          {}        -> {}     -> Truthy (different from python)
          []        -> []     -> Truthy (different from python)
          everything else is truthy
    '''
    if v is False:
        return False
    elif v is None:
        return False
    elif v == 0:
        return False
    else:
        # everything else is truthy!
        return True