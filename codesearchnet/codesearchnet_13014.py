def vcfheader(data, names, ofile):
    """
    Prints header for vcf files
    """
    ## choose reference string
    if data.paramsdict["reference_sequence"]:
        reference = data.paramsdict["reference_sequence"]
    else:
        reference = "pseudo-reference (most common base at site)"


    ##FILTER=<ID=minCov,Description="Data shared across <{mincov} samples">
    ##FILTER=<ID=maxSH,Description="Heterozygosous site shared across >{maxsh} samples">
    header = """\
##fileformat=VCFv4.0
##fileDate={date}
##source=ipyrad_v.{version}
##reference={reference}
##phasing=unphased
##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
##FORMAT=<ID=CATG,Number=1,Type=String,Description="Base Counts (CATG)">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{names}
""".format(date=time.strftime("%Y/%m/%d"),
           version=__version__,
           reference=os.path.basename(reference),
           mincov=data.paramsdict["min_samples_locus"],
           maxsh=data.paramsdict["max_shared_Hs_locus"],
           names="\t".join(names))
    ## WRITE
    ofile.write(header)