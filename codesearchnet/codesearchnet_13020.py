def tree_panel_plot(ttree,
    print_args=False,
    *args, 
    **kwargs):
    """
    signature...
    """

    ## create Panel plot object and set height & width
    panel = Panel(ttree)          #tree, edges, verts, names)
    if not kwargs.get("width"):
        panel.kwargs["width"] = min(1000, 25*len(panel.tree))
    if not kwargs.get("height"):
        panel.kwargs["height"] = panel.kwargs["width"]

    ## update defaults with kwargs & update size based on ntips & ntests
    panel.kwargs.update(kwargs)

    ## magic node label arguments overrides others
    if panel.kwargs["show_node_support"]:
        nnodes = sum(1 for i in panel.tree.traverse()) - len(panel.tree)
        ## set node values
        supps = [int(panel.tree.search_nodes(idx=j)[0].support) \
                 for j in range(nnodes)]
        if not panel.kwargs["vsize"]:
            panel.kwargs["vsize"] = 20
        sizes = [panel.kwargs["vsize"] for j in range(nnodes)]
        ## add leaf values
        supps += [""] * len(panel.tree)
        sizes += [0] * len(panel.tree)
        ## override args
        panel.kwargs["vlabel"] = supps
        panel.kwargs["vsize"] = sizes
        panel.kwargs["vlshow"] = True
        #panel.kwargs["vmarker"] = 's'  ## square
        ## if unrooted then hide root node scores
        if len(panel.tree.children) > 2:
            supps[0] = ""
            sizes[0] = 0
        #print(panel.kwargs["vlabels"])
        #print(panel.kwargs["vsize"])
    elif panel.kwargs.get("vlabel"):
        panel.kwargs["vlabel"] = panel.kwargs["vlabel"]
        panel.kwargs["vlshow"] = True
    else:
        panel.kwargs["vlabel"] = panel.node_labels.keys() #names.keys()

    ## debugger / see all options
    if print_args:
        print(panel.kwargs)

    ## maybe add panels for plotting tip traits in the future
    ## ...

    ## create a canvas and a single cartesian coord system
    canvas = toyplot.Canvas(height=panel.kwargs['height'], width=panel.kwargs['width'])
    axes = canvas.cartesian(bounds=("10%", "90%", "10%", "90%"))    
    axes.show = panel.kwargs["show_axes"]
    
    ## add panel plots to the axis
    panel._panel_tree(axes)
    if panel.kwargs["show_tip_labels"]:
        panel._panel_tip_labels(axes)

    return canvas, axes, panel