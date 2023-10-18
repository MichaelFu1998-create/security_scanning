def loose_in(pl,k):
    '''
        pl = ['bcd','xabcxx','x','y']
        loose_in(pl,'abc')
        
    '''
    cond = some(pl,lambda ele:(k in ele))['cond']
    return(cond)