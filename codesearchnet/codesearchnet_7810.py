def _build_input_args(input_filepath_list, input_format_list):
    ''' Builds input arguments by stitching input filepaths and input
    formats together.
    '''
    if len(input_format_list) != len(input_filepath_list):
        raise ValueError(
            "input_format_list & input_filepath_list are not the same size"
        )

    input_args = []
    zipped = zip(input_filepath_list, input_format_list)
    for input_file, input_fmt in zipped:
        input_args.extend(input_fmt)
        input_args.append(input_file)

    return input_args