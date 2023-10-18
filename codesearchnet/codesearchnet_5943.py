def get_internet_gateway(vpc, **conn):
    """Gets the Internet Gateway details about a VPC"""
    result = {}
    ig_result = describe_internet_gateways(Filters=[{"Name": "attachment.vpc-id", "Values": [vpc["id"]]}], **conn)

    if ig_result:
        # Only 1 IG can be attached to a VPC:
        result.update({
            "State": ig_result[0]["Attachments"][0]["State"],
            "Id": ig_result[0]["InternetGatewayId"],
            "Tags": ig_result[0].get("Tags", [])
        })

    return result