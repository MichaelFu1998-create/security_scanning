def get_route_tables(vpc, **conn):
    """Gets the VPC Route Tables"""
    route_tables = describe_route_tables(Filters=[{"Name": "vpc-id", "Values": [vpc["id"]]}], **conn)

    rt_ids = []
    for r in route_tables:
        rt_ids.append(r["RouteTableId"])

    return rt_ids