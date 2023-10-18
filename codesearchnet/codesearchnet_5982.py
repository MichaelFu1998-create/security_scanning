def get_server_certificate(server_certificate, flags=FLAGS.BASE, **conn):
    """
    Orchestrates all the calls required to fully build out an IAM User in the following format:

    {
        "Arn": ...,
        "ServerCertificateName": ...,
        "Path": ...,
        "ServerCertificateId": ...,
        "UploadDate": ...,  # str
        "Expiration": ...,  # str
        "CertificateBody": ...,
        "CertificateChain": ...,
        "_version": 1
    }

    :param flags: By default, Users is disabled. This is somewhat expensive as it has to call the
                  `get_server_certificate` call multiple times.
    :param server_certificate: dict MUST contain the ServerCertificateName and also a combination of
                               either the ARN or the account_number.
    :param output: Determines whether keys should be returned camelized or underscored.
    :param conn: dict containing enough information to make a connection to the desired account.
                 Must at least have 'assume_role' key.
    :return: dict containing fully built out Server Certificate.
    """
    if not server_certificate.get('ServerCertificateName'):
        raise MissingFieldException('Must include ServerCertificateName.')

    server_certificate = modify(server_certificate, output='camelized')
    _conn_from_args(server_certificate, conn)
    return registry.build_out(flags, start_with=server_certificate, pass_datastructure=True, **conn)