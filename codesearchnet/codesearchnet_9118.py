def merge(mer_inputs=MER_INPUTS, mer_output=MER_OUTPUT):
    """
    merge the phrase files into one file
    :param mer_inputs: the phrase files
    :param mer_output: the output file
    :return: None
    """
    dirname = os.path.dirname(__file__)
    output_file = os.path.join(dirname, DICT_DIRECTORY, mer_output)
    lines = []
    for in_file in MER_INPUTS:
        input_file = os.path.join(dirname, DICT_DIRECTORY, in_file)
        with open(input_file, encoding='utf-8') as f:
            for line in f:
                lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)