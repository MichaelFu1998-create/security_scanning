def _compute_stats(self, start, ipyclient, quiet=False):
        """
        Compute sampling stats and consens trees. 
        """
        
        ## get name indices
        names = self.samples

        ## make a consensus from bootstrap reps.
        if self.checkpoint.boots:
            tre = ete3.Tree(self.trees.tree, format=0)
            tre.unroot()
            with open(self.trees.boots, 'r') as inboots:
                bb = [ete3.Tree(i.strip(), format=0) for i in inboots.readlines()]
                bb = [tre] + bb

            ## calculate consensus supports
            ctre, counts = consensus_tree(bb, names=names)
            self.trees.cons = os.path.join(self.dirs, self.name+".cons")
            with open(self.trees.cons, 'w') as ocons:
                ocons.write(ctre.write(format=0))

        else:
            ctre = ete3.Tree(self.trees.tree, format=0)
            ctre.unroot()

        ## build stats file and write trees
        self.trees.nhx = os.path.join(self.dirs, self.name+".nhx")
        lbview = ipyclient.load_balanced_view()
        qtots = {}
        qsamp = {}
        tots = sum(1 for i in ctre.iter_leaves())
        totn = set(ctre.get_leaf_names())

        ## iterate over node traversal
        for node in ctre.traverse():
            ## this is slow, needs to look at every sampled quartet
            ## so we send it to be processed on engines
            qtots[node] = lbview.apply(get_total, *(tots, node))
            qsamp[node] = lbview.apply(get_sampled, *(self, totn, node))

        ## wait for jobs to finish (+1 to lenjob is for final progress printer)
        alljobs = qtots.values() + qsamp.values()
        lenjobs = len(alljobs) + 1
        printstr = "calculating stats | {} | "
        done = 0
        while 1:
            if not quiet:
                done = sum([i.ready() for i in alljobs])
                elapsed = datetime.timedelta(seconds=int(time.time()-start))
                progressbar(lenjobs, done, 
                    printstr.format(elapsed), spacer="")
            if (lenjobs - 1) == done:
                break
            else:
                time.sleep(0.1)
        ## store results in the tree object
        for node in ctre.traverse():
            total = qtots[node].result()
            sampled = qsamp[node].result()
            node.add_feature("quartets_total", total)
            node.add_feature("quartets_sampled", sampled)
        features = ["quartets_total", "quartets_sampled"]

        ## update final progress
        elapsed = datetime.timedelta(seconds=int(time.time()-start))        
        progressbar(1, 1, printstr.format(elapsed), spacer="")
        if not quiet:
            print("")

        ## write tree in NHX format 
        with open(self.trees.nhx, 'w') as outtre:
            outtre.write(ctre.write(format=0, features=features))