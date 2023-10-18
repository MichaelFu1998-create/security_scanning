def _simulate(self, nreps, admix=None, Ns=500000, gen=20):
    """
    Enter a baba.Tree object in which the 'tree' attribute (newick 
    derived tree) has edge lengths in units of generations. You can 
    use the 'gen' parameter to multiply branch lengths by a constant. 

    Parameters:
    -----------

    nreps: (int)
        Number of reps (loci) to simulate under the demographic scenario
    tree: (baba.Tree object)
        A baba.Tree object initialized by calling baba.Tree(*args). 
    admix: (list)
        A list of admixture events to occur on the tree. Nodes must be 
        reference by their index number, and events must occur in time
        intervals when edges exist. Use the .draw() function of the 
        baba.Tree object to see node index numbers and coalescent times.
    Ns: (float)
        Fixed effective population size for all lineages (may allow to vary
        in the future). 
    gen: (int)
        A multiplier applied to branch lengths to scale into units of 
        generations. Example, if all edges on a tree were 1 then you might
        enter 50000 to multiply so that edges are 50K generations long.

    """

    ## node ages
    Taus = np.array(list(set(self.verts[:, 1]))) * 1e4 * gen

    ## The tips samples, ordered alphanumerically
    ## Population IDs correspond to their indexes in pop config
    ntips = len(self.tree)
    #names = {name: idx for idx, name in enumerate(sorted(self.tree.get_leaf_names()))}
    ## rev ladderized leaf name order (left to right on downward facing tree)
    names = {name: idx for idx, name in enumerate(self.tree.get_leaf_names()[::-1])}
    pop_config = [
        ms.PopulationConfiguration(sample_size=2, initial_size=Ns)
        for i in range(ntips)
    ]

    ## migration matrix all zeros init
    migmat = np.zeros((ntips, ntips)).tolist()

    ## a list for storing demographic events
    demog = []

    ## coalescent times
    coals = sorted(list(set(self.verts[:, 1])))[1:]
    for ct in xrange(len(coals)):
        ## check for admix event before next coalescence
        ## ...
        
        ## print coals[ct], nidxs, time
        nidxs = np.where(self.verts[:, 1] == coals[ct])[0]
        time = Taus[ct+1]

        ## add coalescence at each node
        for nidx in nidxs:
            node = self.tree.search_nodes(name=str(nidx))[0]

            ## get destionation (lowest child idx number), and other
            dest = sorted(node.get_leaves(), key=lambda x: x.idx)[0]
            otherchild = [i for i in node.children if not 
                          i.get_leaves_by_name(dest.name)][0]

            ## get source
            if otherchild.is_leaf():
                source = otherchild
            else:
                source = sorted(otherchild.get_leaves(), key=lambda x: x.idx)[0]
            
            ## add coal events
            event = ms.MassMigration(
                        time=int(time),
                        source=names[source.name], 
                        destination=names[dest.name], 
                        proportion=1.0)
            #print(int(time), names[source.name], names[dest.name])
        
            ## ...
            demog.append(event)
            
            
    ## sim the data
    replicates = ms.simulate(
        population_configurations=pop_config,
        migration_matrix=migmat,
        demographic_events=demog,
        num_replicates=nreps,
        length=100, 
        mutation_rate=1e-8)
    return replicates