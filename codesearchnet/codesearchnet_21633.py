def sorted_refer_to(l,referer,reverse=False,**kwargs):
    '''
        from elist.elist import *
        l = ["a","b","c"]
        referer = [7,8,6]
        sorted_refer_to(l,referer)
        {'list': ['c', 'a', 'b'], 'referer': [6, 7, 8]}
        l
        referer
        >>>
    '''
    if("mode" in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "both"
    tl =[]
    length = l.__len__()
    for i in range(0,length):
        ele = (l[i],referer[i])
        tl.append(ele)
    tl = sorted(tl,key=itemgetter(1),reverse=reverse)
    sorted_l =[]
    sorted_r = []
    for i in range(0,length):
        sorted_l.append(tl[i][0])
        sorted_r.append(tl[i][1])
    if(mode == "only-list"):
        return(sorted_l)
    elif(mode == "only-referer"):
        return(referer)
    else:
        return({"list":sorted_l,"referer":sorted_r})