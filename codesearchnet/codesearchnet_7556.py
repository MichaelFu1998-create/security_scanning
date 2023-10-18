def data_two_freqs(N=200):
    """A simple test example with two close frequencies

    """
    nn = arange(N)
    xx = cos(0.257*pi*nn) + sin(0.2*pi*nn) + 0.01*randn(nn.size)
    return xx