def _clean(zipcode, valid_length=_valid_zipcode_length):
    """ Assumes zipcode is of type `str` """
    zipcode = zipcode.split("-")[0]  # Convert #####-#### to #####

    if len(zipcode) != valid_length:
        raise ValueError(
            'Invalid format, zipcode must be of the format: "#####" or "#####-####"'
        )

    if _contains_nondigits(zipcode):
        raise ValueError('Invalid characters, zipcode may only contain digits and "-".')

    return zipcode