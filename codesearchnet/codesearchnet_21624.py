def uniform_index(index,length):
    '''
        uniform_index(0,3)
        uniform_index(-1,3)
        uniform_index(-4,3)
        uniform_index(-3,3)
        uniform_index(5,3)
    '''
    if(index<0):
        rl = length+index
        if(rl<0):
            index = 0
        else:
            index = rl
    elif(index>=length):
        index = length
    else:
        index = index
    return(index)