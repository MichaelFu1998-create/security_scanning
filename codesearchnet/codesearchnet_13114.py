def result_files(self):
        """ returns a list of files that have finished structure """
        reps = OPJ(self.workdir, self.name+"-K-*-rep-*_f")
        repfiles = glob.glob(reps)
        return repfiles