def _raiseIfNotStr(s):
    '''internal'''
    if s is not None and not isinstance(s, string_types):
        raise PyEXception('Cannot use type %s' % str(type(s)))