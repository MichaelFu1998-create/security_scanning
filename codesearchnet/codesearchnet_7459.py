def get_common_prefix(z):
    """Get common directory in a zip file if any."""
    name_list = z.namelist()
    if name_list and all(n.startswith(name_list[0]) for n in name_list[1:]):
        return name_list[0]
    return None