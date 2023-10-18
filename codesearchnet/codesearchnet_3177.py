def viz_trace(view):
    """
    Given a Manticore trace file, highlight the basic blocks.
    """
    tv = TraceVisualizer(view, None)
    if tv.workspace is None:
        tv.workspace = get_workspace()
    tv.visualize()