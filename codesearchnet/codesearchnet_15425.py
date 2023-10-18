def _insert_tree(cursor, tree, parent_id=None, index=0, is_collated=False):
    """Inserts a binder tree into the archive."""
    if isinstance(tree, dict):
        if tree['id'] == 'subcol':
            document_id = None
            title = tree['title']
        else:
            cursor.execute("""\
            SELECT module_ident, name
            FROM modules
            WHERE ident_hash(uuid,major_version,minor_version) = %s
            """, (tree['id'],))
            try:
                document_id, document_title = cursor.fetchone()
            except TypeError:  # NoneType
                raise ValueError("Missing published document for '{}'."
                                 .format(tree['id']))
            if tree.get('title', None):
                title = tree['title']
            else:
                title = document_title
        # TODO We haven't settled on a flag (name or value)
        #      to pin the node to a specific version.
        is_latest = True
        cursor.execute(TREE_NODE_INSERT,
                       dict(document_id=document_id, parent_id=parent_id,
                            title=title, child_order=index,
                            is_latest=is_latest, is_collated=is_collated))
        node_id = cursor.fetchone()[0]
        if 'contents' in tree:
            _insert_tree(cursor, tree['contents'], parent_id=node_id,
                         is_collated=is_collated)
    elif isinstance(tree, list):
        for tree_node in tree:
            _insert_tree(cursor, tree_node, parent_id=parent_id,
                         index=tree.index(tree_node), is_collated=is_collated)