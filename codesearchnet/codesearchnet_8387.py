def get_sizeof_descriptor_table(version="Denali"):
    """
    Get sizeof DescriptorTable
    """
    if version == "Denali":
        return sizeof(DescriptorTableDenali)
    elif version == "Spec20":
        return sizeof(DescriptorTableSpec20)
    elif version == "Spec12":
        return 0
    else:
        raise RuntimeError("Error version!")