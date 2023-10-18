def originFormat_listOfDicts(l):
    """Return [{},{},{}] as a 2d matrix."""
    titles=[]
    for d in l:
        for k in d.keys():
            if not k in titles:
                titles.append(k)
    titles.sort()
    data=np.empty((len(l),len(titles)))*np.nan
    for y in range(len(l)):
        for x in range(len(titles)):
            if titles[x] in l[y].keys():
                data[y][x]=l[y][titles[x]]
    return titles,data