def render(node, strict=False):
    """Recipe to render a given FST node.

    The FST is composed of branch nodes which are either lists or dicts
    and of leaf nodes which are strings. Branch nodes can have other
    list, dict or leaf nodes as childs.

    To render a string, simply output it. To render a list, render each
    of its elements in order. To render a dict, you must follow the
    node's entry in the nodes_rendering_order dictionary and its
    dependents constraints.

    This function hides all this algorithmic complexity by returning
    a structured rendering recipe, whatever the type of node. But even
    better, you should subclass the RenderWalker which simplifies
    drastically working with the rendered FST.

    The recipe is a list of steps, each step correspond to a child and is actually a 3-uple composed of the following fields:

    - `key_type` is a string determining the type of the child in the second field (`item`) of the tuple. It can be one of:

      - 'constant': the child is a string
      - 'node': the child is a dict
      - 'key': the child is an element of a dict
      - 'list': the child is a list
      - 'formatting': the child is a list specialized in formatting

    - `item` is the child itself: either a string, a dict or a list.
    - `render_key` gives the key used to access this child from the parent node. It's a string if the node is a dict or a number if its a list.

    Please note that "bool" `key_types` are never rendered, that's why
    they are not shown here.
    """
    if isinstance(node, list):
        return render_list(node)

    elif isinstance(node, dict):
        return render_node(node, strict=strict)

    else:
        raise NotImplementedError("You tried to render a %s. Only list and dicts can be rendered." % node.__class__.__name__)