def _call_structure(mname, ename, sname, name, workdir, seed, ntaxa, nsites, kpop, rep):
    """ make the subprocess call to structure """
    ## create call string
    outname = os.path.join(workdir, "{}-K-{}-rep-{}".format(name, kpop, rep))

    cmd = ["structure", 
           "-m", mname, 
           "-e", ename, 
           "-K", str(kpop),
           "-D", str(seed), 
           "-N", str(ntaxa), 
           "-L", str(nsites),
           "-i", sname, 
           "-o", outname]

    ## call the shell function
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT)
    comm = proc.communicate()

    ## cleanup
    oldfiles = [mname, ename, sname]
    for oldfile in oldfiles:
        if os.path.exists(oldfile):
            os.remove(oldfile)
    return comm