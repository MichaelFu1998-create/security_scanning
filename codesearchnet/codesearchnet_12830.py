def draw(self, axes):
        """
        Returns a treemix plot on a toyplot.axes object. 
        """            
        ## create a toytree object from the treemix tree result
        tre = toytree.tree(newick=self.results.tree)
        tre.draw(
            axes=axes,
            use_edge_lengths=True,
            tree_style='c',
            tip_labels_align=True,
            edge_align_style={"stroke-width": 1}
        );

        ## get coords 
        for admix in self.results.admixture:
            ## parse admix event
            pidx, pdist, cidx, cdist, weight = admix
            a = _get_admix_point(tre, pidx, pdist)
            b = _get_admix_point(tre, cidx, cdist)

            ## add line for admixture edge
            mark = axes.plot(
                a = (a[0], b[0]),
                b = (a[1], b[1]),
                style={"stroke-width": 10*weight,
                       "stroke-opacity": 0.95, 
                       "stroke-linecap": "round"}
            )

            ## add points at admixture sink
            axes.scatterplot(
                a = (b[0]),
                b = (b[1]),
                size=8,
                title="weight: {}".format(weight),
            )

        ## add scale bar for edge lengths
        axes.y.show=False
        axes.x.ticks.show=True
        axes.x.label.text = "Drift parameter"
        return axes