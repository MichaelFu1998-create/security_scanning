def parent(groups,ID):
    """given a groups dictionary and an ID, return its actual parent ID."""
    if ID in groups.keys():
        return ID # already a parent
    if not ID in groups.keys():
        for actualParent in groups.keys():
            if ID in groups[actualParent]:
                return actualParent # found the actual parent
    return None