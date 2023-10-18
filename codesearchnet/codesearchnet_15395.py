def _reassemble_binder(id, tree, metadata):
    """Reassemble a Binder object coming out of the database."""
    binder = cnxepub.Binder(id, metadata=metadata)
    for item in tree['contents']:
        node = _node_to_model(item, parent=binder)
        if node.metadata['title'] != item['title']:
            binder.set_title_for_node(node, item['title'])
    return binder