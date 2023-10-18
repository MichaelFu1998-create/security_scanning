def regex_in(pl,regex):
    '''
        regex = re.compile("^[a-z]+$")
        pl = ['b1c3d','xab15cxx','1x','y2']
        regex_in(pl,regex)
        
        regex = re.compile("^[0-9a-z]+$")
        pl = ['b1c3d','xab15cxx','1x','y2']
        regex_in(pl,regex)
        
    '''
    def cond_func(ele,regex):
        m = regex.search(ele)
        if(m == None):
            return(False)
        else:
            return(True)
    cond = some(pl,cond_func,regex)['cond']
    return(cond)