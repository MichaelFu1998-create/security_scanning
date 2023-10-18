def spDiff(SP1,SP2):
    """
    Function that compares two spatial pooler instances. Compares the
    static variables between the two poolers to make sure that they are equivalent.

    Parameters
    -----------------------------------------
    SP1 first spatial pooler to be compared

    SP2 second spatial pooler to be compared

    To establish equality, this function does the following:

    1.Compares the connected synapse matrices for each coincidence

    2.Compare the potential synapse matrices for each coincidence

    3.Compare the permanence matrices for each coincidence

    4.Compare the firing boosts between the two poolers.

    5.Compare the duty cycles before and after inhibition for both poolers

    """
    if(len(SP1._masterConnectedM)!=len(SP2._masterConnectedM)):
        print "Connected synapse matrices are different sizes"
        return False

    if(len(SP1._masterPotentialM)!=len(SP2._masterPotentialM)):
        print "Potential synapse matrices are different sizes"
        return False

    if(len(SP1._masterPermanenceM)!=len(SP2._masterPermanenceM)):
        print "Permanence matrices are different sizes"
        return False


    #iterate over cells
    for i in range(0,len(SP1._masterConnectedM)):
        #grab the Coincidence Matrices and compare them
        connected1 = SP1._masterConnectedM[i]
        connected2 = SP2._masterConnectedM[i]
        if(connected1!=connected2):
            print "Connected Matrices for cell %d different"  % (i)
            return False
        #grab permanence Matrices and compare them
        permanences1 = SP1._masterPermanenceM[i];
        permanences2 = SP2._masterPermanenceM[i];
        if(permanences1!=permanences2):
            print "Permanence Matrices for cell %d different" % (i)
            return False
        #grab the potential connection Matrices and compare them
        potential1 = SP1._masterPotentialM[i];
        potential2 = SP2._masterPotentialM[i];
        if(potential1!=potential2):
            print "Potential Matrices for cell %d different" % (i)
            return False

    #Check firing boosts
    if(not numpy.array_equal(SP1._firingBoostFactors,SP2._firingBoostFactors)):
        print "Firing boost factors are different between spatial poolers"
        return False

    #Check duty cycles after inhibiton
    if(not numpy.array_equal(SP1._dutyCycleAfterInh,SP2._dutyCycleAfterInh)):
        print "Duty cycles after inhibition are different between spatial poolers"
        return False


    #Check duty cycles before inhibition
    if(not numpy.array_equal(SP1._dutyCycleBeforeInh,SP2._dutyCycleBeforeInh)):
        print "Duty cycles before inhibition are different between spatial poolers"
        return False


    print("Spatial Poolers are equivalent")

    return True