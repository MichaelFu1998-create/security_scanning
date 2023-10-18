def library_supports_api(library_version, api_version, different_major_breaks_support=True):
    """
    Returns whether api_version is supported by given library version.
    E. g.  library_version (1,3,21) returns True for api_version (1,3,21), (1,3,19), (1,3,'x'), (1,2,'x'), (1, 'x')
           False for (1,3,24), (1,4,'x'), (2,'x')

    different_major_breaks_support - if enabled and library and api major versions are different always return False
           ex) with library_version (2,0,0) and for api_version(1,3,24) returns False if enabled, True if disabled
    """
    assert isinstance(library_version, (tuple, list))  # won't work with e.g. generators
    assert len(library_version) == 3
    sequence_type = type(library_version)  # assure we will compare same types
    api_version = sequence_type(0 if num == 'x' else num for num in api_version)
    if different_major_breaks_support and library_version[0] != api_version[0]:
        return False
    assert len(api_version) <= 3     # otherwise following comparision won't work as intended, e.g. (2, 0, 0) > (2, 0, 0, 0)
    return library_version >= api_version