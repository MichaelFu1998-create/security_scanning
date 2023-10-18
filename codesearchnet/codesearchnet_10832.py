def from_bin(bin_array):
    """
    Convert binary array back a nonnegative integer. The array length is 
    the bit width. The first input index holds the MSB and the last holds the LSB.
    """
    width = len(bin_array)
    bin_wgts = 2**np.arange(width-1,-1,-1)
    return int(np.dot(bin_array,bin_wgts))