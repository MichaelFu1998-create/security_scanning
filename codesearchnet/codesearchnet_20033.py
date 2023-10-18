def abfGroupFiles(groups,folder):
    """
    when given a dictionary where every key contains a list of IDs, replace
    the keys with the list of files matching those IDs. This is how you get a
    list of files belonging to each child for each parent.
    """
    assert os.path.exists(folder)
    files=os.listdir(folder)
    group2={}
    for parent in groups.keys():
        if not parent in group2.keys():
            group2[parent]=[]
        for ID in groups[parent]:
            for fname in [x.lower() for x in files if ID in x.lower()]:
                group2[parent].extend([fname])
    return group2