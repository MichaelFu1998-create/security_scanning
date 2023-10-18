def baseId(resource_id, return_version=False):
    """Calculate base id and version from a resource id.

    :params resource_id: Resource id.
    :params return_version: (optional) True if You need version, returns (resource_id, version).
    """
    version = 0
    resource_id = resource_id + 0xC4000000  # 3288334336
    # TODO: version is broken due ^^, needs refactoring

    while resource_id > 0x01000000:  # 16777216
        version += 1
        if version == 1:
            resource_id -= 0x80000000  # 2147483648  # 0x50000000  # 1342177280 ?  || 0x2000000  # 33554432
        elif version == 2:
            resource_id -= 0x03000000  # 50331648
        else:
            resource_id -= 0x01000000  # 16777216

    if return_version:
        return resource_id, version - 67  # just correct "magic number"

    return resource_id