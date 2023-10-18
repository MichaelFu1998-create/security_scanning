def dummyListOfDicts(size=100):
    """
    returns a list (of the given size) of dicts with fake data.
    some dictionary keys are missing for some of the items.
    """
    titles="ahp,halfwidth,peak,expT,expI,sweep".split(",")
    ld=[] #list of dicts
    for i in range(size):
        d={}
        for t in titles:
            if int(np.random.random(1)*100)>5: #5% of values are missing
                d[t]=float(np.random.random(1)*100) #random number 0-100
            if t=="sweep" and "sweep" in d.keys():
                d[t]=int(d[t])
        ld.append(d)
    return ld