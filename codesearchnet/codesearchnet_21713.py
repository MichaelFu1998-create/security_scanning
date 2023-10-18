def split(ol,value,**kwargs):
    '''
        ol = ['a',1,'a',2,'a',3,'a',4,'a']
        split(ol,'a')
        split(ol,'a',whiches=[0])
        split(ol,'a',whiches=[1])
        split(ol,'a',whiches=[2])
        split(ol,'a',whiches=[0,2])
        ol = [1,'a',2,'a',3,'a',4]
        split(ol,'a')
        split('x=bcdsef=g','=',whiches=[0])
        
    '''
    if('whiches' in kwargs):
        whiches = kwargs['whiches']    
    else:
        whiches = None
    indexes =  indexes_all(ol,value)
    if(whiches == None):
        pass
    else:
        indexes = select_indexes(indexes,whiches)
    rslt = []
    rslt.append(ol[:indexes[0]])
    si = indexes[0]+1
    for i in range(1,indexes.__len__()):
        ei = indexes[i]
        ele = ol[si:ei]
        rslt.append(ele)
        si = ei + 1
    ele = ol[si:ol.__len__()]
    rslt.append(ele)
    return(rslt)