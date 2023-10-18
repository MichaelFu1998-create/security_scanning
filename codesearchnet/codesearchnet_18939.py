def guess_array_memory_usage( bam_readers, dtype, use_strand=False ):
    """Returns an estimate for the maximum amount of memory to be consumed by numpy arrays."""
    ARRAY_COUNT = 5
    if not isinstance( bam_readers, list ):
        bam_readers = [ bam_readers ]
    if isinstance( dtype, basestring ):
        dtype = NUMPY_DTYPES.get( dtype, None )
    use_strand = use_strand + 1 #if false, factor of 1, if true, factor of 2
    dtypes = guess_numpy_dtypes_from_idxstats( bam_readers, default=None, force_dtype=False )
    if not [ dt for dt in dtypes if dt is not None ]:
        #found no info from idx
        dtypes = guess_numpy_dtypes_from_idxstats( bam_readers, default=dtype or numpy.uint64, force_dtype=True )
    elif dtype:
        dtypes = [ dtype if dt else None for dt in dtypes ]
    read_groups = []
    no_read_group = False
    for bam in bam_readers:
        rgs = bam.get_read_groups()
        if rgs:
            for rg in rgs:
                if rg not in read_groups:
                    read_groups.append( rg )
        else:
            no_read_group = True
    read_groups = len( read_groups ) + no_read_group
    max_ref_size = 0
    array_byte_overhead = sys.getsizeof( numpy.zeros( ( 0 ), dtype=numpy.uint64 ) )
    array_count = ARRAY_COUNT * use_strand * read_groups
    for bam in bam_readers:
        for i, ( name, length ) in enumerate( bam.get_references() ):
            if dtypes[i] is not None:
                max_ref_size = max( max_ref_size, ( length + length * dtypes[i]().nbytes * array_count + ( array_byte_overhead * ( array_count + 1 ) ) ) )
    return max_ref_size