def _validate_file_formats(input_filepath_list, combine_type):
    '''Validate that combine method can be performed with given files.
    Raises IOError if input file formats are incompatible.
    '''
    _validate_sample_rates(input_filepath_list, combine_type)

    if combine_type == 'concatenate':
        _validate_num_channels(input_filepath_list, combine_type)