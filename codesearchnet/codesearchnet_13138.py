def call_fastq_dump_on_SRRs(self, srr, outname, paired):
    """
    calls fastq-dump on SRRs, relabels fastqs by their accession
    names, and writes them to the workdir. Saves temp sra files
    in the designated tmp folder and immediately removes them.
    """

    ## build command for fastq-dumping
    fd_cmd = [
        "fastq-dump", srr,
        "--accession", outname,
        "--outdir", self.workdir, 
        "--gzip",
        ]
    if paired:
        fd_cmd += ["--split-files"]

    ## call fq dump command
    proc = sps.Popen(fd_cmd, stderr=sps.STDOUT, stdout=sps.PIPE)
    o, e = proc.communicate()

    ## delete the stupid temp sra file from the place 
    ## that it is very hard-coded to be written to, and 
    ## LEFT IN, for some crazy reason.
    srafile = os.path.join(self.workdir, "sra", srr+".sra")
    if os.path.exists(srafile):
        os.remove(srafile)