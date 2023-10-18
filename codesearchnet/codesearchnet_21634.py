def batsorted(referer,*lists,**kwargs):
    '''
        from elist.elist import *
        referer = [4,2,3,1]
        l1 = ['a','b','c','d']
        l2 = [100,200,300,400]
        l3 = ['A','B','A','B']
        nl1,nl2,nl3 = batsorted(referer,l1,l2,l3)
        nl1
        nl2
        nl3
        nl1,nl2,nl3 = batsorted(referer,l1,l2,l3,reverse=True)
        nl1
        nl2
        nl3
        ####the batsorted will not modify the original lists
        l1
        l2
        l3
    '''
    if('reverse' in kwargs):
        reverse = kwargs['reverse']
    else:
        reverse = False
    length = referer.__len__()
    indexes = list(range(0,length))
    rslt = sorted_refer_to(indexes,referer,reverse=reverse)
    referer = rslt['referer']
    indexes = rslt['list']
    rslt = []
    lists = copy.deepcopy(list(lists))
    for i in range(0,lists.__len__()):
        l = lists[i]
        nl = []
        for j in range(0,length):
            loc = indexes[j]
            nl.append(l[loc])
        rslt.append(nl)
    return(tuple(rslt))