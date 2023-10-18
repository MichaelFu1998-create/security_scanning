def reorder_sub(ol,sub):
    '''
        sub = ['query', 'params', 'fragment', 'path']
        ol = ['scheme', 'username', 'password', 'hostname', 'port', 'path', 'params', 'query', 'fragment']
        reorder_sub(ol,sub)
    '''
    def cond_func(ele,ol):
        index = ol.index(ele)
        return(index)
    indexes = array_map(sub,cond_func,ol)
    nsub = sorted_refer_to(sub,indexes)['list']
    return(nsub)