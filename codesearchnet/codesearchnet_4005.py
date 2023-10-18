def read_causal_pairs(filename, scale=True, **kwargs):
    """Convert a ChaLearn Cause effect pairs challenge format into numpy.ndarray.

    :param filename: path of the file to read or DataFrame containing the data
    :type filename: str or pandas.DataFrame
    :param scale: Scale the data
    :type scale: bool
    :param kwargs: parameters to be passed to pandas.read_csv
    :return: Dataframe composed of (SampleID, a (numpy.ndarray) , b (numpy.ndarray))
    :rtype: pandas.DataFrame
    """
    def convert_row(row, scale):
        """Convert a CCEPC row into numpy.ndarrays.

        :param row:
        :type row: pandas.Series
        :return: tuple of sample ID and the converted data into numpy.ndarrays
        :rtype: tuple
        """
        a = row["A"].split(" ")
        b = row["B"].split(" ")

        if a[0] == "":
            a.pop(0)
            b.pop(0)
        if a[-1] == "":
            a.pop(-1)
            b.pop(-1)

        a = array([float(i) for i in a])
        b = array([float(i) for i in b])
        if scale:
            a = scaler(a)
            b = scaler(b)
        return row['SampleID'], a, b
    if isinstance(filename, str):
        data = read_csv(filename, **kwargs)
    elif isinstance(filename, DataFrame):
        data = filename
    else:
        raise TypeError("Type not supported.")
    conv_data = []

    for idx, row in data.iterrows():
        conv_data.append(convert_row(row, scale))
    df = DataFrame(conv_data, columns=['SampleID', 'A', 'B'])
    df = df.set_index("SampleID")
    return df