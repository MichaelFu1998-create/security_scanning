def padnames(names):
    """ pads names for loci output """

    ## get longest name
    longname_len = max(len(i) for i in names)
    ## Padding distance between name and seq.
    padding = 5
    ## add pad to names
    pnames = [name + " " * (longname_len - len(name)+ padding) \
              for name in names]
    snppad = "//" + " " * (longname_len - 2 + padding)
    return np.array(pnames), snppad