def _get_evanno_table(self, kpops, max_var_multiple, quiet):
    """
    Calculates Evanno method K value scores for a series
    of permuted clumpp results. 
    """

    ## iterate across k-vals
    kpops = sorted(kpops)
    replnliks = []

    for kpop in kpops:
        ## concat results for k=x
        reps, excluded = _concat_reps(self, kpop, max_var_multiple, quiet)

        ## report if some results were excluded
        if excluded:
            if not quiet:
                sys.stderr.write(
                "[K{}] {} reps excluded (not converged) see 'max_var_multiple'.\n"\
                .format(kpop, excluded))

        if reps:
            ninds = reps[0].inds
            nreps = len(reps)
        else:
            ninds = nreps = 0
        if not reps:
            print "no result files found"

        ## all we really need is the lnlik
        replnliks.append([i.est_lnlik for i in reps])

    ## compare lnlik and var of results
    if len(replnliks) > 1:
        lnmean = [np.mean(i) for i in replnliks]
        lnstds = [np.std(i, ddof=1) for i in replnliks]
    else:
        lnmean = replnliks
        lnstds = np.nan

    tab = pd.DataFrame(
        index=kpops,
        data={
            "Nreps": [len(i) for i in replnliks],
            "lnPK": [0] * len(kpops),
            "lnPPK": [0] * len(kpops),
            "deltaK": [0] * len(kpops),
            "estLnProbMean": lnmean, 
            "estLnProbStdev": lnstds,
        }
        )

    ## calculate Evanno's
    for kpop in kpops[1:]:
        tab.loc[kpop, "lnPK"] = tab.loc[kpop, "estLnProbMean"] \
                              - tab.loc[kpop-1, "estLnProbMean"]

    for kpop in kpops[1:-1]:
        tab.loc[kpop, "lnPPK"] = abs(tab.loc[kpop+1, "lnPK"] 
                                     - tab.loc[kpop, "lnPK"])
        tab.loc[kpop, "deltaK"] = (abs(
                                    tab.loc[kpop+1, "estLnProbMean"] - \
                                    2.0 * tab.loc[kpop, "estLnProbMean"] + \
                                    tab.loc[kpop-1, "estLnProbMean"]) / \
                                   tab.loc[kpop, "estLnProbStdev"])
        
    ## return table
    return tab