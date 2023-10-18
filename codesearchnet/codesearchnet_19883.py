def dual(ABF):
    """Plot two channels of current sweep (top/bottom)."""
    new(ABF)
    pylab.subplot(211)
    pylab.title("Input A (channel 0)")
    ABF.channel=0
    sweep(ABF)
    pylab.subplot(212)
    pylab.title("Input B (channel 1)")
    ABF.channel=1
    sweep(ABF)