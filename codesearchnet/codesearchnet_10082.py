def dump_dh_parameters(dh_parameters, encoding='pem'):
    """
    Serializes an asn1crypto.algos.DHParameters object into a byte string

    :param dh_parameters:
        An asn1crypto.algos.DHParameters object

    :param encoding:
        A unicode string of "pem" or "der"

    :return:
        A byte string of the encoded DH parameters
    """

    if encoding not in set(['pem', 'der']):
        raise ValueError(pretty_message(
            '''
            encoding must be one of "pem", "der", not %s
            ''',
            repr(encoding)
        ))

    if not isinstance(dh_parameters, algos.DHParameters):
        raise TypeError(pretty_message(
            '''
            dh_parameters must be an instance of asn1crypto.algos.DHParameters,
            not %s
            ''',
            type_name(dh_parameters)
        ))

    output = dh_parameters.dump()
    if encoding == 'pem':
        output = pem.armor('DH PARAMETERS', output)
    return output