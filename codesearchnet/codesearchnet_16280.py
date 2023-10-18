def merge_from_store_and_in_mems(from_store, in_mem_shas, dont_update_shas_of):
    """
    If we don't merge the shas from the sha store and if we build a
    subgraph, the .shastore will only contain the shas of the files
    from the subgraph and the rest of the graph will have to be
    rebuilt
    """
    if not from_store:
        for item in dont_update_shas_of:
            if item in in_mem_shas['files']:
                del in_mem_shas['files'][item]
        return in_mem_shas
    for key in from_store['files']:
        if key not in in_mem_shas['files'] and key not in dont_update_shas_of:
            in_mem_shas['files'][key] = from_store['files'][key]
    for item in dont_update_shas_of:
        if item in in_mem_shas['files']:
            del in_mem_shas['files'][item]
    return in_mem_shas