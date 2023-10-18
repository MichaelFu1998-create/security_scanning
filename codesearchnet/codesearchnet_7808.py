def _validate_num_channels(input_filepath_list, combine_type):
    ''' Check if files in input file list have the same number of channels
    '''
    channels = [
        file_info.channels(f) for f in input_filepath_list
    ]
    if not core.all_equal(channels):
        raise IOError(
            "Input files do not have the same number of channels. The "
            "{} combine type requires that all files have the same "
            "number of channels"
            .format(combine_type)
        )