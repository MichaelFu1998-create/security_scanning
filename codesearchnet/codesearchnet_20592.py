def sav_to_pandas_savreader(input_file):
    """
    SPSS .sav files to Pandas DataFrame through savreader module

    :param input_file: string

    :return:
    """
    from savReaderWriter import SavReader
    lines = []
    with SavReader(input_file, returnHeader=True) as reader:
        header = next(reader)
        for line in reader:
            lines.append(line)

    return pd.DataFrame(data=lines, columns=header)