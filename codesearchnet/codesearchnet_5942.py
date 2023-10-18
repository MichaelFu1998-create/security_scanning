def get_classic_link(vpc, **conn):
    """Gets the Classic Link details about a VPC"""
    result = {}

    try:
        cl_result = describe_vpc_classic_link(VpcIds=[vpc["id"]], **conn)[0]
        result["Enabled"] = cl_result["ClassicLinkEnabled"]

        # Check for DNS as well:
        dns_result = describe_vpc_classic_link_dns_support(VpcIds=[vpc["id"]], **conn)[0]
        result["DnsEnabled"] = dns_result["ClassicLinkDnsSupported"]
    except ClientError as e:
        # This is not supported for all regions.
        if 'UnsupportedOperation' not in str(e):
            raise e

    return result