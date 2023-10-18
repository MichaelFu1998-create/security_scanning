def baba_panel_plot(
    ttree,
    tests, 
    boots,
    show_tip_labels=True, 
    show_test_labels=True, 
    use_edge_lengths=False, 
    collapse_outgroup=False, 
    pct_tree_x=0.4, 
    pct_tree_y=0.2,
    alpha=3.0,
    *args, 
    **kwargs):
    """
    signature...
    """

    ## create Panel plot object and set height & width
    bootsarr = np.array(boots)
    panel = Panel(ttree, tests, bootsarr, alpha)
    if not kwargs.get("width"):
        panel.kwargs["width"] = min(1000, 50*len(panel.tree))
    if not kwargs.get("height"):
        panel.kwargs["height"] = min(1000, 50*len(panel.tests))   

    ## update defaults with kwargs & update size based on ntips & ntests
    kwargs.update(dict(pct_tree_x=pct_tree_x, pct_tree_y=pct_tree_y))
    panel.kwargs.update(kwargs)

    ## create a canvas and a single cartesian coord system
    canvas = toyplot.Canvas(height=panel.kwargs['height'], width=panel.kwargs['width'])
    axes = canvas.cartesian(bounds=("10%", "90%", "5%", "95%"))    
    axes.show = False

    ## add panels to axes
    panel.panel_tree(axes)
    panel.panel_test(axes)
    panel.panel_tip_labels(axes)
    if isinstance(boots, np.ndarray):
        panel.panel_results(axes)
    return canvas, axes, panel