def validate_input_file_list(input_filepath_list):
    '''Input file list validation function. Checks that object is a list and
    contains valid filepaths that can be processed by SoX.

    Parameters
    ----------
    input_filepath_list : list
        A list of filepaths.

    '''
    if not isinstance(input_filepath_list, list):
        raise TypeError("input_filepath_list must be a list.")
    elif len(input_filepath_list) < 2:
        raise ValueError("input_filepath_list must have at least 2 files.")

    for input_filepath in input_filepath_list:
        validate_input_file(input_filepath)