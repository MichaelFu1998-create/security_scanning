def _validate_sample_rates(input_filepath_list, combine_type):
    ''' Check if files in input file list have the same sample rate
    '''
    sample_rates = [
        file_info.sample_rate(f) for f in input_filepath_list
    ]
    if not core.all_equal(sample_rates):
        raise IOError(
            "Input files do not have the same sample rate. The {} combine "
            "type requires that all files have the same sample rate"
            .format(combine_type)
        )