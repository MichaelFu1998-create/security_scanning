def levdown(anxt, enxt=None):
    """One step backward Levinson recursion

    :param anxt:
    :param enxt:
    :return:
        * acur the P'th order prediction polynomial based on the P+1'th order prediction polynomial, anxt.
        * ecur the the P'th order prediction error  based on the P+1'th order prediction error, enxt.

    ..  * knxt the P+1'th order reflection coefficient.

    """
    #% Some preliminaries first
    #if nargout>=2 & nargin<2
    #    raise ValueError('Insufficient number of input arguments');
    if anxt[0] != 1:
        raise ValueError('At least one of the reflection coefficients is equal to one.')
    anxt = anxt[1:] #  Drop the leading 1, it is not needed
                    #  in the step down

    # Extract the k+1'th reflection coefficient
    knxt = anxt[-1]
    if knxt == 1.0:
        raise ValueError('At least one of the reflection coefficients is equal to one.')

    # A Matrix formulation from Stoica is used to avoid looping
    acur = (anxt[0:-1]-knxt*numpy.conj(anxt[-2::-1]))/(1.-abs(knxt)**2)
    ecur = None
    if enxt is not None:
        ecur = enxt/(1.-numpy.dot(knxt.conj().transpose(),knxt))

    acur = numpy.insert(acur, 0, 1)

    return acur, ecur