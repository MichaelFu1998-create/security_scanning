def _finalize_stats(self, ipyclient):
        """ write final tree files """

        ## print stats file location:
        #print(STATSOUT.format(opr(self.files.stats)))

        ## print finished tree information ---------------------
        print(FINALTREES.format(opr(self.trees.tree)))

        ## print bootstrap information --------------------------
        if self.params.nboots:
            ## get consensus, map values to tree edges, record stats file
            self._compute_tree_stats(ipyclient)
            ## print bootstrap info
            print(BOOTTREES.format(opr(self.trees.cons), opr(self.trees.boots))) 

        ## print the ASCII tree only if its small
        if len(self.samples) < 20:
            if self.params.nboots:
                wctre = ete3.Tree(self.trees.cons, format=0)
                wctre.ladderize()
                print(wctre.get_ascii(show_internal=True, 
                                      attributes=["dist", "name"]))
                print("")
            else:
                qtre = ete3.Tree(self.trees.tree, format=0)
                qtre.ladderize()
                #qtre = toytree.tree(self.trees.tree, format=0)
                #qtre.tree.unroot()
                print(qtre.get_ascii())
                print("")

        ## print PDF filename & tips -----------------------------
        docslink = "https://toytree.readthedocs.io/"    
        citelink = "https://ipyrad.readthedocs.io/tetrad.html"
        print(LINKS.format(docslink, citelink))