def get_base(vpc, **conn):
    """
    The base will return:
    - ARN
    - Region
    - Name
    - Id
    - Tags
    - IsDefault
    - InstanceTenancy
    - CidrBlock
    - CidrBlockAssociationSet
    - Ipv6CidrBlockAssociationSet
    - DhcpOptionsId
    - Attributes
    - _version

    :param bucket_name:
    :param conn:
    :return:
    """
    # Get the base:
    base_result = describe_vpcs(VpcIds=[vpc["id"]], **conn)[0]

    # The name of the VPC is in the tags:
    vpc_name = None
    for t in base_result.get("Tags", []):
        if t["Key"] == "Name":
            vpc_name = t["Value"]

    dhcp_opts = None
    # Get the DHCP Options:
    if base_result.get("DhcpOptionsId"):
        # There should only be exactly 1 attached to a VPC:
        dhcp_opts = describe_dhcp_options(DhcpOptionsIds=[base_result["DhcpOptionsId"]], **conn)[0]["DhcpOptionsId"]

    # Get the Attributes:
    attributes = {}
    attr_vals = [
        ("EnableDnsHostnames", "enableDnsHostnames"),
        ("EnableDnsSupport", "enableDnsSupport")
    ]
    for attr, query in attr_vals:
        attributes[attr] = describe_vpc_attribute(VpcId=vpc["id"], Attribute=query, **conn)[attr]

    vpc.update({
        'name': vpc_name,
        'region': conn["region"],
        'tags': base_result.get("Tags", []),
        'is_default': base_result["IsDefault"],
        'instance_tenancy': base_result["InstanceTenancy"],
        'dhcp_options_id': dhcp_opts,
        'cidr_block': base_result["CidrBlock"],
        'cidr_block_association_set': base_result.get("CidrBlockAssociationSet", []),
        'ipv6_cidr_block_association_set': base_result.get("Ipv6CidrBlockAssociationSet", []),
        'attributes': attributes,
        '_version': 1
    })
    return vpc