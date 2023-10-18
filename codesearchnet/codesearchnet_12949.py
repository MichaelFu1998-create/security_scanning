def make( data, samples ):
    """ Convert vcf from step6 to .loci format to facilitate downstream format conversion """
    invcffile   =  os.path.join( data.dirs.consens, data.name+".vcf" )
    outlocifile  =  os.path.join( data.dirs.outfiles, data.name+".loci" )

    importvcf( invcffile, outlocifile )