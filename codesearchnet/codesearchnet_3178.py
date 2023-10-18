def viz_live_trace(view):
    """
    Given a Manticore trace file, highlight the basic blocks.
    """
    tv = TraceVisualizer(view, None, live=True)
    if tv.workspace is None:
        tv.workspace = get_workspace()
    # update due to singleton in case we are called after a clear
    tv.live_update = True
    tv.visualize()