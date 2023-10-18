def compute_tree_stats(self, ipyclient):
    """ 
    compute stats for stats file and NHX tree features
    """

    ## get name indices
    names = self.samples

    ## get majority rule consensus tree of weighted Q bootstrap trees
    if self.params.nboots:
        
        ## Tree object
        fulltre = ete3.Tree(self.trees.tree, format=0)
        fulltre.unroot()

        ## only grab as many boots as the last option said was max
        with open(self.trees.boots, 'r') as inboots:
            bb = [ete3.Tree(i.strip(), format=0) for i in inboots.readlines()]
            wboots = [fulltre] + bb[-self.params.nboots:]
        
        ## infer consensus tree and write to file
        wctre, wcounts = consensus_tree(wboots, names=names)
        self.trees.cons = os.path.join(self.dirs, self.name + ".cons")
        with open(self.trees.cons, 'w') as ocons:
            ocons.write(wctre.write(format=0))
    else:
        wctre = ete3.Tree(self.trees.tree, format=0)
        wctre.unroot()

    ## build stats file and write trees
    self.trees.nhx = os.path.join(self.dirs, self.name + ".nhx")
    with open(self.files.stats, 'w') as ostats:

        ## print Tetrad info
        #ostats.write(STATS_STRING.format(**self.stats))

        ## print bootstrap splits
        if self.params.nboots:
            ostats.write("## splits observed in {} trees\n".format(len(wboots)))
            for i, j in enumerate(self.samples):
                ostats.write("{:<3} {}\n".format(i, j))
            ostats.write("\n")
            for split, freq in wcounts:
                if split.count('1') > 1:
                    ostats.write("{}   {:.2f}\n".format(split, round(freq, 2)))
            ostats.write("\n")

    ## parallelized this function because it can be slogging
    lbview = ipyclient.load_balanced_view()
    
    ## store results in dicts
    qtots = {}
    qsamp = {}
    tots = sum(1 for i in wctre.iter_leaves())
    totn = set(wctre.get_leaf_names())

    ## iterate over node traversal. 
    for node in wctre.traverse():
        ## this is slow, needs to look at every sampled quartet
        ## so we send it be processed on an engine
        qtots[node] = lbview.apply(_get_total, *(tots, node))
        qsamp[node] = lbview.apply(_get_sampled, *(self, totn, node))

    ## wait for jobs to finish
    ipyclient.wait()

    ## put results into tree
    for node in wctre.traverse():
        ## this is fast, just calcs n_choose_k
        total = qtots[node].result()
        sampled = qsamp[node].result()
        ## store the results to the tree            
        node.add_feature("quartets_total", total)
        node.add_feature("quartets_sampled", sampled)
    features = ["quartets_total", "quartets_sampled"]

    ## return as NHX format with extra info
    with open(self.trees.nhx, 'w') as outtre:
        outtre.write(wctre.write(format=0, features=features))