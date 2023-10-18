def getStr_to_pathlist(gs):
    '''
        gs = "[1]['1'][2]"
        getStr_to_pathlist(gs)
        gs = "['u']['u1']"
        getStr_to_pathlist(gs)
    '''
    def numize(w):
        try:
            int(w)
        except:
            try:
                float(w)
            except:
                return(w)
            else:
                return(float(w))
        else:
           return(int(w))
    def strip_quote(w):
        if(type(w) == type('')):
            if(w[0]==w[-1]):
                if((w[0]=="'") |(w[0]=='"')):
                    return(w[1:-1])
                else:
                    return(w)
            else:
                return(w)
        else:
            return(w)
    gs = gs[1:-1]
    pl = gs.split("][")
    pl = array_map(pl,numize)
    pl = array_map(pl,strip_quote)
    return(pl)