def concat_vcf(data, names, full):
    """
    Sorts, concatenates, and gzips VCF chunks. Also cleans up chunks.
    """
    ## open handle and write headers
    if not full:
        writer = open(data.outfiles.vcf, 'w')
    else:
        writer = gzip.open(data.outfiles.VCF, 'w')
    vcfheader(data, names, writer)
    writer.close()

    ## get vcf chunks
    vcfchunks = glob.glob(data.outfiles.vcf+".*")
    vcfchunks.sort(key=lambda x: int(x.rsplit(".")[-1]))

    ## concatenate
    if not full:
        writer = open(data.outfiles.vcf, 'a')
    else:
        writer = gzip.open(data.outfiles.VCF, 'a')

    ## what order do users want? The order in the original ref file?
    ## Sorted by the size of chroms? that is the order in faidx.
    ## If reference mapping then it's nice to sort the vcf data by
    ## CHROM and POS. This is doing a very naive sort right now, so the
    ## CHROM will be ordered, but not the pos within each chrom.
    if data.paramsdict["assembly_method"] in ["reference", "denovo+reference"]:
        ## Some unix sorting magic to get POS sorted within CHROM
        ## First you sort by POS (-k 2,2), then you do a `stable` sort 
        ## by CHROM. You end up with POS ordered and grouped correctly by CHROM
        ## but relatively unordered CHROMs (locus105 will be before locus11).
        cmd = ["cat"] + vcfchunks + [" | sort -k 2,2 -n | sort -k 1,1 -s"]
        cmd = " ".join(cmd)
        proc = sps.Popen(cmd, shell=True, stderr=sps.STDOUT, stdout=writer, close_fds=True)
    else:
        proc = sps.Popen(["cat"] + vcfchunks, stderr=sps.STDOUT, stdout=writer, close_fds=True)

    err = proc.communicate()[0]
    if proc.returncode:
        raise IPyradWarningExit("err in concat_vcf: %s", err)
    writer.close()

    for chunk in vcfchunks:
        os.remove(chunk)