def _conn_from_arn(arn):
    """
    Extracts the account number from an ARN.
    :param arn: Amazon ARN containing account number.
    :return: dictionary with a single account_number key that can be merged with an existing
    connection dictionary containing fields such as assume_role, session_name, region.
    """
    arn = ARN(arn)
    if arn.error:
        raise CloudAuxException('Bad ARN: {arn}'.format(arn=arn))
    return dict(
        account_number=arn.account_number,
    )