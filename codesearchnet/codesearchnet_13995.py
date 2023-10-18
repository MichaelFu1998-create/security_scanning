def create(iterations=1000, distance=1.0, layout=LAYOUT_SPRING, depth=True):
    
    """ Returns a new graph with predefined styling.
    """

    #global _ctx
   
        
    _ctx.colormode(_ctx.RGB)
    g = graph(iterations, distance, layout)
   
    
    # Styles for different types of nodes.
    s = style.style
    g.styles.append(s(style.LIGHT    , _ctx, fill   = _ctx.color(0.0, 0.0, 0.0, 0.20)))
    g.styles.append(s(style.DARK     , _ctx, fill   = _ctx.color(0.3, 0.5, 0.7, 0.75)))
    g.styles.append(s(style.BACK     , _ctx, fill   = _ctx.color(0.5, 0.8, 0.0, 0.50)))
    g.styles.append(s(style.IMPORTANT, _ctx, fill   = _ctx.color(0.3, 0.6, 0.8, 0.75)))
    g.styles.append(s(style.HIGHLIGHT, _ctx, stroke = _ctx.color(1.0, 0.0, 0.5), strokewidth=1.5))
    g.styles.append(s(style.MARKED   , _ctx))
    g.styles.append(s(style.ROOT     , _ctx, text   = _ctx.color(1.0, 0.0, 0.4, 1.00), 
                                             stroke = _ctx.color(0.8, 0.8, 0.8, 0.60),
                                             strokewidth = 1.5, 
                                             fontsize    = 16, 
                                             textwidth   = 150))

    # Important nodes get a double stroke.
    def important_node(s, node, alpha=1.0):
        style.style(None, _ctx).node(s, node, alpha)
        r = node.r * 1.4
        _ctx.nofill()
        _ctx.oval(node.x-r, node.y-r, r*2, r*2)  

    # Marked nodes have an inner dot.
    def marked_node(s, node, alpha=1.0):
        style.style(None, _ctx).node(s, node, alpha)
        r = node.r * 0.3
        _ctx.fill(s.stroke)
        _ctx.oval(node.x-r, node.y-r, r*2, r*2)
    
    g.styles.important.node = important_node
    g.styles.marked.node = marked_node 
    
    g.styles.depth = depth

    # Styling guidelines. All nodes have the default style, except:
    # 1) a node directly connected to the root gets the LIGHT style.
    # 2) a node with more than 4 edges gets the DARK style.
    # 3) a node with a weight of 0.75-1.0 gets the IMPORTANT style.
    # 4) the graph.root node gets the ROOT style.
    # 5) the node last clicked gets the BACK style.    
    g.styles.guide.append(style.LIGHT     , lambda graph, node: graph.root in node.links)
    g.styles.guide.append(style.DARK      , lambda graph, node: len(node.links) > 4)
    g.styles.guide.append(style.IMPORTANT , lambda graph, node: node.weight > 0.75)
    g.styles.guide.append(style.ROOT      , lambda graph, node: node == graph.root)
    g.styles.guide.append(style.BACK      , lambda graph, node: node == graph.events.clicked)
    
    # An additional rule applies every node's weight to its radius.
    def balance(graph, node): 
        node.r = node.r*0.75 + node.r*node.weight*0.75
    g.styles.guide.append("balance", balance)
    
    # An additional rule that keeps leaf nodes closely clustered.
    def cluster(graph, node):
        if len(node.links) == 1: 
            node.links.edge(node.links[0]).length *= 0.5
    g.styles.guide.append("cluster", cluster)
    
    g.styles.guide.order = [
        style.LIGHT, style.DARK, style.IMPORTANT, style.ROOT, style.BACK, "balance", "nurse"
    ]

    return g