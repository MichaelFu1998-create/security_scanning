def lowpass(data,filterSize=None):
    """
    minimal complexity low-pass filtering.
    Filter size is how "wide" the filter will be.
    Sigma will be 1/10 of this filter width.
    If filter size isn't given, it will be 1/10 of the data size.
    """
    if filterSize is None:
        filterSize=len(data)/10
    kernel=kernel_gaussian(size=filterSize)
    data=convolve(data,kernel) # do the convolution with padded edges
    return data