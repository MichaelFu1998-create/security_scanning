def comprise(list1,list2,**kwargs):
    '''
        from elist.elist import *
        comprise([1,2,3,4,5],[2,3,4],mode="loose")
        comprise([1,2,3,4,5],[2,3,4])
        comprise([1,2,3,4,5],[2,3,4],mode="strict")
        comprise([1,2,3,4,5],[1,2,3,4],mode="strict")
        #not recursive ,only one level
        #please refer to ListTree.search for recursive support
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = "loose"
    len_1 = list1.__len__()
    len_2 = list2.__len__()
    if(len_2>len_1):
        return(False)
    else:
        if(mode=="strict"):
            if(list2 == list1[:len_2]):
                return(True)
            else:
                return(False)
        else:
            end = len_1 - len_2
            for i in range(0,end+1):
                if(list2 == list1[i:(i+len_2)]):
                    return(True)
                else:
                    pass
    return(False)