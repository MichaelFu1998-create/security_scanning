def _build_input_format_list(input_filepath_list, input_volumes=None,
                             input_format=None):
    '''Set input formats given input_volumes.

    Parameters
    ----------
    input_filepath_list : list of str
        List of input files
    input_volumes : list of float, default=None
        List of volumes to be applied upon combining input files. Volumes
        are applied to the input files in order.
        If None, input files will be combined at their original volumes.
    input_format : list of lists, default=None
        List of input formats to be applied to each input file. Formatting
        arguments are applied to the input files in order.
        If None, the input formats will be inferred from the file header.

    '''
    n_inputs = len(input_filepath_list)
    input_format_list = []
    for _ in range(n_inputs):
        input_format_list.append([])

    # Adjust length of input_volumes list
    if input_volumes is None:
        vols = [1] * n_inputs
    else:
        n_volumes = len(input_volumes)
        if n_volumes < n_inputs:
            logger.warning(
                'Volumes were only specified for %s out of %s files.'
                'The last %s files will remain at their original volumes.',
                n_volumes, n_inputs, n_inputs - n_volumes
            )
            vols = input_volumes + [1] * (n_inputs - n_volumes)
        elif n_volumes > n_inputs:
            logger.warning(
                '%s volumes were specified but only %s input files exist.'
                'The last %s volumes will be ignored.',
                n_volumes, n_inputs, n_volumes - n_inputs
            )
            vols = input_volumes[:n_inputs]
        else:
            vols = [v for v in input_volumes]

    # Adjust length of input_format list
    if input_format is None:
        fmts = [[] for _ in range(n_inputs)]
    else:
        n_fmts = len(input_format)
        if n_fmts < n_inputs:
            logger.warning(
                'Input formats were only specified for %s out of %s files.'
                'The last %s files will remain unformatted.',
                n_fmts, n_inputs, n_inputs - n_fmts
            )
            fmts = [f for f in input_format]
            fmts.extend([[] for _ in range(n_inputs - n_fmts)])
        elif n_fmts > n_inputs:
            logger.warning(
                '%s Input formats were specified but only %s input files exist'
                '. The last %s formats will be ignored.',
                n_fmts, n_inputs, n_fmts - n_inputs
            )
            fmts = input_format[:n_inputs]
        else:
            fmts = [f for f in input_format]

    for i, (vol, fmt) in enumerate(zip(vols, fmts)):
        input_format_list[i].extend(['-v', '{}'.format(vol)])
        input_format_list[i].extend(fmt)

    return input_format_list