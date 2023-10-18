def get_vpc_peering_connections(vpc, **conn):
    """Gets the Internet Gateway details about a VPC"""
    accepter_result = describe_vpc_peering_connections(Filters=[{"Name": "accepter-vpc-info.vpc-id",
                                                                 "Values": [vpc["id"]]}], **conn)

    requester_result = describe_vpc_peering_connections(Filters=[{"Name": "requester-vpc-info.vpc-id",
                                                                 "Values": [vpc["id"]]}], **conn)

    # Assuming that there will be no duplicates:
    peer_ids = []
    for peering in accepter_result + requester_result:
        peer_ids.append(peering["VpcPeeringConnectionId"])

    return peer_ids