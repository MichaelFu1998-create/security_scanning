def _compare_node_lists(old, new):
    '''
    Investigate two lists of workflow TreeNodes and categorize them.

    There will be three types of nodes after categorization:
        1. Nodes that only exists in the new list. These nodes will later be
        created recursively.
        2. Nodes that only exists in the old list. These nodes will later be
        deleted recursively.
        3. Node pairs that makes an exact match. These nodes will be further
        investigated.

    Corresponding nodes of old and new lists will be distinguished by their
    unified_job_template value. A special case is that both the old and the new
    lists contain one type of node, say A, and at least one of them contains
    duplicates. In this case all A nodes in the old list will be categorized as
    to-be-deleted and all A nodes in the new list will be categorized as
    to-be-created.
    '''
    to_expand = []
    to_delete = []
    to_recurse = []
    old_records = {}
    new_records = {}
    for tree_node in old:
        old_records.setdefault(tree_node.unified_job_template, [])
        old_records[tree_node.unified_job_template].append(tree_node)
    for tree_node in new:
        new_records.setdefault(tree_node.unified_job_template, [])
        new_records[tree_node.unified_job_template].append(tree_node)
    for ujt_id in old_records:
        if ujt_id not in new_records:
            to_delete.extend(old_records[ujt_id])
            continue
        old_list = old_records[ujt_id]
        new_list = new_records.pop(ujt_id)
        if len(old_list) == 1 and len(new_list) == 1:
            to_recurse.append((old_list[0], new_list[0]))
        else:
            to_delete.extend(old_list)
            to_expand.extend(new_list)
    for nodes in new_records.values():
        to_expand.extend(nodes)
    return to_expand, to_delete, to_recurse