def get_vpc(vpc_id, flags=FLAGS.ALL, **conn):
    """
    Orchestrates all the calls required to fully fetch details about a VPC:

    {
        "Arn": ...,
        "Region": ...,
        "Name": ...,
        "Id": ...,
        "Tags: ...,
        "VpcPeeringConnections": ...,
        "ClassicLink": ...,
        "DhcpOptionsId": ...,
        "InternetGateway": ...,
        "IsDefault": ...,
        "CidrBlock": ...,
        "CidrBlockAssociationSet": ...,
        "Ipv6CidrBlockAssociationSet": ...,
        "InstanceTenancy": ...,
        "RouteTables": ...,
        "NetworkAcls": ...,
        "FlowLogs": ...,
        "Subnets": ...,
        "Attributes": ...,
        "FlowLogs": ...,
        "_version": 1
    }

    :param vpc_id: The ID of the VPC
    :param flags:
    :param conn:
    :return:
    """
    # Is the account number that's passed in the same as in the connection dictionary?
    if not conn.get("account_number"):
        raise CloudAuxException({"message": "Must supply account number in the connection dict to construct "
                                            "the VPC ARN.",
                                 "vpc_id": vpc_id})

    if not conn.get("region"):
        raise CloudAuxException({"message": "Must supply region in the connection dict to construct "
                                            "the VPC ARN.",
                                 "vpc_id": vpc_id})

    start = {
        'arn': "arn:aws:ec2:{region}:{account}:vpc/{vpc_id}".format(region=conn["region"],
                                                                    account=conn["account_number"],
                                                                    vpc_id=vpc_id),
        'id': vpc_id
    }

    return registry.build_out(flags, start_with=start, pass_datastructure=True, **conn)