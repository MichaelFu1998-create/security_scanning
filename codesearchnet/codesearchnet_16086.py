def caf_to_fastq(infile, outfile, min_length=0, trim=False):
    '''Convert a CAF file to fastq. Reads shorter than min_length are not output. If clipping information is in the CAF file (with a line Clipping QUAL ...) and trim=True, then trim the reads'''
    caf_reader = caf.file_reader(infile)
    fout = utils.open_file_write(outfile)

    for c in caf_reader:
        if trim:
            if c.clip_start is not None and c.clip_end is not None:
                c.seq.seq = c.seq.seq[c.clip_start:c.clip_end + 1]
                c.seq.qual = c.seq.qual[c.clip_start:c.clip_end + 1]
            else:
                print('Warning: no clipping info for sequence', c.id, file=sys.stderr)


        if len(c.seq) >= min_length:
            print(c.seq, file=fout)

    utils.close(fout)