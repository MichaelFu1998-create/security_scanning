def get_network_acls(vpc, **conn):
    """Gets the VPC Network ACLs"""
    route_tables = describe_network_acls(Filters=[{"Name": "vpc-id", "Values": [vpc["id"]]}], **conn)

    nacl_ids = []
    for r in route_tables:
        nacl_ids.append(r["NetworkAclId"])

    return nacl_ids