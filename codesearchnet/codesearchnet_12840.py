def _name_from_file(fname, splitnames, fields):
    """ internal func: get the sample name from any pyrad file """
    ## allowed extensions
    file_extensions = [".gz", ".fastq", ".fq", ".fasta", ".clustS", ".consens"]
    base, _ = os.path.splitext(os.path.basename(fname))

    ## remove read number from name
    base = base.replace("_R1_.", ".")\
               .replace("_R1_", "")\
               .replace("_R1.", ".")

    ## remove extensions, retains '.' in file names.
    while 1:
        tmpb, tmpext = os.path.splitext(base)
        if tmpext in file_extensions:        
            base = tmpb
        else:
            break

    if fields:
        namebits = base.split(splitnames)
        base = []
        for field in fields:
            try:
                base.append(namebits[field])
            except IndexError:
                pass
        base = splitnames.join(base)

    if not base:
        raise IPyradError("""
    Found invalid/empty filename in link_fastqs. Check splitnames argument.
    """)

    return base