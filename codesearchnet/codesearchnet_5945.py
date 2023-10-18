def get_subnets(vpc, **conn):
    """Gets the VPC Subnets"""
    subnets = describe_subnets(Filters=[{"Name": "vpc-id", "Values": [vpc["id"]]}], **conn)

    s_ids = []
    for s in subnets:
        s_ids.append(s["SubnetId"])

    return s_ids