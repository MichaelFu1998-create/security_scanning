def _concat_reps(self, kpop, max_var_multiple, quiet, **kwargs):
    """
    Combine structure replicates into a single indfile, 
    returns nreps, ninds. Excludes reps with too high of 
    variance (set with max_variance_multiplier) to exclude
    runs that did not converge. 
    """
   
    ## make an output handle
    outf = os.path.join(self.workdir, 
        "{}-K-{}.indfile".format(self.name, kpop))
    
    ## combine replicates and write to indfile
    excluded = 0
    reps = []
    with open(outf, 'w') as outfile:
        repfiles = glob.glob(
            os.path.join(self.workdir, 
                self.name+"-K-{}-rep-*_f".format(kpop)))

        ## get result as a Rep object
        for rep in repfiles:
            result = Rep(rep, kpop=kpop)
            reps.append(result)

        ## exclude results with variance NX above (min) 
        newreps = []
        if len(reps) > 1:
            min_var_across_reps = np.min([i.var_lnlik for i in reps])
        else:
            min_var_across_reps = reps[0].var_lnlik

        ## iterate over reps
        for rep in reps:

            ## store result w/o filtering
            if not max_var_multiple:
                newreps.append(rep)
                outfile.write(rep.stable)

            ## use max-var-multiple as a filter for convergence                
            else:
                #print(
                #    rep.var_lnlik, 
                #    min_var_across_reps, 
                #    rep.var_lnlik / min_var_across_reps, 
                #    max_var_multiple)
                ## e.g., repvar is 1.05X minvar. We keep it if maxvar <= 1.05
                if (rep.var_lnlik / min_var_across_reps) <= max_var_multiple:
                    newreps.append(rep)
                    outfile.write(rep.stable)
                else:
                    excluded += 1

    return newreps, excluded