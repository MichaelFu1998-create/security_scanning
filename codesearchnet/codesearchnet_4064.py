def loads(s):
    '''
        Deserializes a string and converts it to a dictionary. The contents
        of the string must either be JSON or HCL.
        
        :returns: Dictionary 
    '''
    s = u(s)
    if isHcl(s):
        return HclParser().parse(s)
    else:
        return json.loads(s)