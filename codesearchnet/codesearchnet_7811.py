def _validate_volumes(input_volumes):
    '''Check input_volumes contains a valid list of volumes.

    Parameters
    ----------
    input_volumes : list
        list of volume values. Castable to numbers.

    '''
    if not (input_volumes is None or isinstance(input_volumes, list)):
        raise TypeError("input_volumes must be None or a list.")

    if isinstance(input_volumes, list):
        for vol in input_volumes:
            if not core.is_number(vol):
                raise ValueError(
                    "Elements of input_volumes must be numbers: found {}"
                    .format(vol)
                )