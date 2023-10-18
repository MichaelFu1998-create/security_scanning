def _reformat_policy(policy):
    """
    Policies returned from boto3 are massive, ugly, and difficult to read.
    This method flattens and reformats the policy.

    :param policy: Result from invoking describe_load_balancer_policies(...)
    :return: Returns a tuple containing policy_name and the reformatted policy dict.
    """
    policy_name = policy['PolicyName']
    ret = {}
    ret['type'] = policy['PolicyTypeName']
    attrs = policy['PolicyAttributeDescriptions']

    if ret['type'] != 'SSLNegotiationPolicyType':
        return policy_name, ret

    attributes = dict()
    for attr in attrs:
        attributes[attr['AttributeName']] = attr['AttributeValue']

    ret['protocols'] = dict()
    ret['protocols']['sslv2'] = bool(attributes.get('Protocol-SSLv2'))
    ret['protocols']['sslv3'] = bool(attributes.get('Protocol-SSLv3'))
    ret['protocols']['tlsv1'] = bool(attributes.get('Protocol-TLSv1'))
    ret['protocols']['tlsv1_1'] = bool(attributes.get('Protocol-TLSv1.1'))
    ret['protocols']['tlsv1_2'] = bool(attributes.get('Protocol-TLSv1.2'))
    ret['server_defined_cipher_order'] = bool(attributes.get('Server-Defined-Cipher-Order'))
    ret['reference_security_policy'] = attributes.get('Reference-Security-Policy', None)

    non_ciphers = [
        'Server-Defined-Cipher-Order',
        'Protocol-SSLv2',
        'Protocol-SSLv3',
        'Protocol-TLSv1',
        'Protocol-TLSv1.1',
        'Protocol-TLSv1.2',
        'Reference-Security-Policy'
    ]

    ciphers = []
    for cipher in attributes:
        if attributes[cipher] == 'true' and cipher not in non_ciphers:
            ciphers.append(cipher)

    ciphers.sort()
    ret['supported_ciphers'] = ciphers

    return policy_name, ret