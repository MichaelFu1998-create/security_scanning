def _get_clumpp_table(self, kpop, max_var_multiple, quiet):
    """ private function to clumpp results"""

    ## concat results for k=x
    reps, excluded = _concat_reps(self, kpop, max_var_multiple, quiet)
    if reps:
        ninds = reps[0].inds
        nreps = len(reps)
    else:
        ninds = nreps = 0
    if not reps:
        return "no result files found"

    clumphandle = os.path.join(self.workdir, "tmp.clumppparams.txt")
    self.clumppparams.kpop = kpop
    self.clumppparams.c = ninds
    self.clumppparams.r = nreps
    with open(clumphandle, 'w') as tmp_c:
        tmp_c.write(self.clumppparams._asfile())
    
    ## create CLUMPP args string
    outfile = os.path.join(self.workdir, 
                "{}-K-{}.outfile".format(self.name, kpop))
    indfile = os.path.join(self.workdir, 
                "{}-K-{}.indfile".format(self.name, kpop))
    miscfile = os.path.join(self.workdir, 
                "{}-K-{}.miscfile".format(self.name, kpop))
    cmd = ["CLUMPP", clumphandle, 
           "-i", indfile,
           "-o", outfile, 
           "-j", miscfile,
           "-r", str(nreps), 
           "-c", str(ninds), 
           "-k", str(kpop)]

    ## call clumpp
    proc = subprocess.Popen(cmd, 
                            stderr=subprocess.STDOUT, 
                            stdout=subprocess.PIPE)
    _ = proc.communicate()

    ## cleanup
    for rfile in [indfile, miscfile]:
        if os.path.exists(rfile):
            os.remove(rfile)

    ## parse clumpp results file
    ofile = os.path.join(self.workdir, "{}-K-{}.outfile".format(self.name, kpop))
    if os.path.exists(ofile):
        csvtable = pd.read_csv(ofile, delim_whitespace=True, header=None)
        table = csvtable.loc[:, 5:]
    
        ## apply names to cols and rows
        table.columns = range(table.shape[1])
        table.index = self.labels
        if not quiet:
            sys.stderr.write(
                "[K{}] {}/{} results permuted across replicates (max_var={}).\n"\
                .format(kpop, nreps, nreps+excluded, max_var_multiple))
        return table

    else:
        sys.stderr.write("No files ready for {}-K-{} in {}\n"\
                         .format(self.name, kpop, self.workdir))
        return