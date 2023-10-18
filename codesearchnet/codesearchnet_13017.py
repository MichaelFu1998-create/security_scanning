def _collapse_outgroup(tree, taxdicts):
    """ collapse outgroup in ete Tree for easier viewing """
    ## check that all tests have the same outgroup
    outg = taxdicts[0]["p4"]
    if not all([i["p4"] == outg for i in taxdicts]):
        raise Exception("no good")
   
    ## prune tree, keep only one sample from outgroup
    tre = ete.Tree(tree.write(format=1)) #tree.copy(method="deepcopy")
    alltax = [i for i in tre.get_leaf_names() if i not in outg]
    alltax += [outg[0]]
    tre.prune(alltax)
    tre.search_nodes(name=outg[0])[0].name = "outgroup"
    tre.ladderize()

    ## remove other ougroups from taxdicts
    taxd = copy.deepcopy(taxdicts)
    newtaxdicts = []
    for test in taxd:
        #test["p4"] = [outg[0]]
        test["p4"] = ["outgroup"]
        newtaxdicts.append(test)

    return tre, newtaxdicts