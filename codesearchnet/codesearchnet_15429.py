def publish_collated_tree(cursor, tree):
    """Publish a given collated `tree` (containing newly added
    `CompositeDocument` objects and number inforation)
    alongside the original tree.

    """
    tree = _insert_tree(cursor, tree, is_collated=True)
    return tree