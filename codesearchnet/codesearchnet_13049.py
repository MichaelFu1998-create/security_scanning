def get_binom(base1, base2, estE, estH):
    """
    return probability of base call
    """
        
    prior_homo = (1. - estH) / 2.
    prior_hete = estH
    
    ## calculate probs
    bsum = base1 + base2
    hetprob = scipy.misc.comb(bsum, base1)/(2. **(bsum))
    homoa = scipy.stats.binom.pmf(base2, bsum, estE)
    homob = scipy.stats.binom.pmf(base1, bsum, estE)
    
    ## calculate probs
    hetprob *= prior_hete
    homoa *= prior_homo
    homob *= prior_homo
    
    ## final 
    probabilities = [homoa, homob, hetprob]
    bestprob = max(probabilities)/float(sum(probabilities))

    ## return
    if hetprob > homoa:
        return True, bestprob
    else:
        return False, bestprob