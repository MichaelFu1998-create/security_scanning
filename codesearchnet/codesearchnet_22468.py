def run(self,
            proc: Callable[[Optional[str], Optional[str], argparse.Namespace], Optional[bool]],
            file_filter: Optional[Callable[[str], bool]]=None,
            file_filter_2: Optional[Callable[[Optional[str], str, argparse.Namespace], bool]]=None) \
            -> Tuple[int, int]:
        """ Run the directory list processor calling a function per file.
        :param proc: Process to invoke. Args: input_file_name, output_file_name, argparse options. Return pass or fail.
                     No return also means pass
        :param file_filter: Additional filter for testing file names, types, etc.
        :param file_filter_2: File filter that includes directory, filename and opts
                        (separate for backwards compatibility)
        :return: tuple - (number of files passed to proc: int, number of files that passed proc)
        """
        nfiles = 0
        nsuccess = 0

        # List of one or more input and output files
        if self.opts.infile:
            for file_idx in range(len(self.opts.infile)):
                in_f = self.opts.infile[file_idx]
                if self._check_filter(in_f, self.opts.indir, file_filter, file_filter_2):
                    fn = os.path.join(self.opts.indir, in_f) if self.opts.indir else in_f
                    nfiles += 1
                    if self._call_proc(proc, fn, self._outfile_name('', fn, outfile_idx=file_idx)):
                        nsuccess += 1
                    elif self.opts.stoponerror:
                        return nfiles, nsuccess

        # Single input from the command line
        elif not self.opts.indir:
            if self._check_filter(None, None, file_filter, file_filter_2):
                nfiles += 1
                if self._call_proc(proc, None, self._outfile_name('', '')):
                    nsuccess += 1

        # Input directory that needs to be navigated
        else:
            for dirpath, _, filenames in os.walk(self.opts.indir):
                for fn in filenames:
                    if self._check_filter(fn, dirpath, file_filter, file_filter_2):
                        nfiles += 1
                        if self._call_proc(proc, os.path.join(dirpath, fn), self._outfile_name(dirpath, fn)):
                            nsuccess += 1
                        elif self.opts.stoponerror:
                            return nfiles, nsuccess

        return nfiles, nsuccess