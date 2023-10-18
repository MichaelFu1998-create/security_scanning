def get_barcode_func(data, longbar):
    """ returns the fastest func given data & longbar"""
    ## build func for finding barcode
    if longbar[1] == 'same':
        if data.paramsdict["datatype"] == '2brad':
            def getbarcode(cutters, read1, longbar):
                """ find barcode for 2bRAD data """
                return read1[1][:-(len(cutters[0][0]) + 1)][-longbar[0]:]

        else:
            def getbarcode(_, read1, longbar):
                """ finds barcode for invariable length barcode data """
                return read1[1][:longbar[0]]
    else:
        def getbarcode(cutters, read1, longbar):
            """ finds barcode for variable barcode lengths"""
            return findbcode(cutters, longbar, read1)
    return getbarcode