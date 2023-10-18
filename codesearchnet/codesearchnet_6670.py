def bubble_at_T(zs, Psats, fugacities=None, gammas=None):
    '''
    >>> bubble_at_T([0.5, 0.5], [1400, 7000])
    4200.0
    >>> bubble_at_T([0.5, 0.5], [1400, 7000], gammas=[1.1, .75])
    3395.0
    >>> bubble_at_T([0.5, 0.5], [1400, 7000], gammas=[1.1, .75], fugacities=[.995, 0.98])
    3452.440775305097
    '''
    if not fugacities:
        fugacities = [1 for i in range(len(Psats))]
    if not gammas:
        gammas = [1 for i in range(len(Psats))]
    if not none_and_length_check((zs, Psats, fugacities, gammas)):
        raise Exception('Input dimentions are inconsistent or some input parameters are missing.')
    P = sum(zs[i]*Psats[i]*gammas[i]/fugacities[i] for i in range(len(zs)))
    return P