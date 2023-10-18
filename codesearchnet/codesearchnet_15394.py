def _node_to_model(tree_or_item, metadata=None, parent=None,
                   lucent_id=cnxepub.TRANSLUCENT_BINDER_ID):
    """Given a tree, parse to a set of models"""
    if 'contents' in tree_or_item:
        # It is a binder.
        tree = tree_or_item
        binder = cnxepub.TranslucentBinder(metadata=tree)
        for item in tree['contents']:
            node = _node_to_model(item, parent=binder,
                                  lucent_id=lucent_id)
            if node.metadata['title'] != item['title']:
                binder.set_title_for_node(node, item['title'])
        result = binder
    else:
        # It is an item pointing at a document.
        item = tree_or_item
        result = cnxepub.DocumentPointer(item['id'], metadata=item)
    if parent is not None:
        parent.append(result)
    return result