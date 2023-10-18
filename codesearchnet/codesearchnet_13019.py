def draw(
        self, 
        show_tip_labels=True, 
        show_node_support=False,
        use_edge_lengths=False, 
        orient="right",
        print_args=False,
        *args,
        **kwargs):
        """
        plot the tree using toyplot.graph. 

        Parameters:
        -----------
            show_tip_labels: bool
                Show tip names from tree.
            use_edge_lengths: bool
                Use edge lengths from newick tree.
            show_node_support: bool
                Show support values at nodes using a set of default 
                options. 

            ...
        """
        ## re-decompose tree for new orient and edges args
        self._decompose_tree(orient=orient, use_edge_lengths=use_edge_lengths)

        ## update kwargs with entered args and all other kwargs
        dwargs = {}
        dwargs["show_tip_labels"] = show_tip_labels
        dwargs["show_node_support"] = show_node_support
        dwargs.update(kwargs)

        ## pass to panel plotter
        canvas, axes, panel = tree_panel_plot(self, print_args, **dwargs)
        return canvas, axes, panel