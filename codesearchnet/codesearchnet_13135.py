def plot(self, 
        show_test_labels=True, 
        use_edge_lengths=True,         
        collapse_outgroup=False, 
        pct_tree_x=0.5, 
        pct_tree_y=0.2,
        subset_tests=None,
        #toytree_kwargs=None,
        *args, 
        **kwargs):

        """ 
        Draw a multi-panel figure with tree, tests, and results 
        
        Parameters:
        -----------
        height: int
        ...

        width: int
        ...

        show_test_labels: bool
        ...

        use_edge_lengths: bool
        ...

        collapse_outgroups: bool
        ...

        pct_tree_x: float
        ...

        pct_tree_y: float
        ...

        subset_tests: list
        ...

        ...

        """

        ## check for attributes
        if not self.newick:
            raise IPyradError("baba plot requires a newick treefile")
        if not self.tests:
            raise IPyradError("baba plot must have a .tests attribute")

        ## ensure tests is a list
        if isinstance(self.tests, dict):
            self.tests = [self.tests]

        ## re-decompose the tree
        ttree = toytree.tree(
            self.newick, 
            orient='down', 
            use_edge_lengths=use_edge_lengths,
            )

        ## subset test to show fewer
        if subset_tests != None:
            #tests = self.tests[subset_tests]
            tests = [self.tests[i] for i in subset_tests]
            boots = self.results_boots[subset_tests]
        else:
            tests = self.tests
            boots = self.results_boots

        ## make the plot
        canvas, axes, panel = baba_panel_plot(
            ttree=ttree,
            tests=tests, 
            boots=boots, 
            show_test_labels=show_test_labels, 
            use_edge_lengths=use_edge_lengths, 
            collapse_outgroup=collapse_outgroup, 
            pct_tree_x=pct_tree_x,
            pct_tree_y=pct_tree_y,
            *args, 
            **kwargs)
        return canvas, axes, panel