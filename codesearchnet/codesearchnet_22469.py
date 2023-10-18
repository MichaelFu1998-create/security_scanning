def _outfile_name(self, dirpath: str, infile: str, outfile_idx: int=0) -> Optional[str]:
        """ Construct the output file name from the input file.  If a single output file was named and there isn't a
        directory, return the output file.
        :param dirpath: Directory path to infile
        :param infile: Name of input file
        :param outfile_idx: Index into output file list (for multiple input/output files)
        :return: Full name of output file or None if output is not otherwise supplied
        """
        if not self.opts.outfile and not self.opts.outdir:
            # Up to the process itself to decide what do do with it
            return None

        if self.opts.outfile:
            # Output file specified - either one aggregate file or a 1 to 1 list
            outfile_element = self.opts.outfile[0] if len(self.opts.outfile) == 1 else self.opts.outfile[outfile_idx]

        elif self.opts.infile:
            # Input file name(s) have been supplied
            if '://' in infile:
                # Input file is a URL -- generate an output file of the form "_url[n]"
                outfile_element = "_url{}".format(outfile_idx + 1)
            else:
                outfile_element = os.path.basename(infile).rsplit('.', 1)[0]

        else:
            # Doing an input directory to an output directory
            relpath = dirpath[len(self.opts.indir) + 1:] if not self.opts.flatten and self.opts.indir else ''
            outfile_element = os.path.join(relpath, os.path.split(infile)[1][:-len(self.infile_suffix)])
        return (os.path.join(self.opts.outdir, outfile_element) if self.opts.outdir else outfile_element) + \
               (self.outfile_suffix if not self.opts.outfile and self.outfile_suffix else '')