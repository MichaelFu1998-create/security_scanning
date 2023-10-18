def levup(acur, knxt, ecur=None):
    """LEVUP  One step forward Levinson recursion

    :param acur:
    :param knxt:
    :return:
        * anxt the P+1'th order prediction polynomial based on the P'th order prediction polynomial, acur, and the
          P+1'th order reflection coefficient, Knxt.
        * enxt the P+1'th order prediction  prediction error, based on the P'th order prediction error, ecur.


    :References:  P. Stoica R. Moses, Introduction to Spectral Analysis  Prentice Hall, N.J., 1997, Chapter 3.
    """
    if acur[0] != 1:
        raise ValueError('At least one of the reflection coefficients is equal to one.')
    acur = acur[1:] #  Drop the leading 1, it is not needed

    # Matrix formulation from Stoica is used to avoid looping
    anxt = numpy.concatenate((acur, [0])) + knxt * numpy.concatenate((numpy.conj(acur[-1::-1]), [1]))

    enxt = None
    if ecur is not None:
        # matlab version enxt = (1-knxt'.*knxt)*ecur
        enxt = (1. - numpy.dot(numpy.conj(knxt), knxt)) * ecur

    anxt = numpy.insert(anxt, 0, 1)

    return anxt, enxt