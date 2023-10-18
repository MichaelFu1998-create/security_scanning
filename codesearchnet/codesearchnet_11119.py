def gng_importer(self, corpus_file):
        """Fill in self.ngcorpus from a Google NGram corpus file.

        Parameters
        ----------
        corpus_file : file
            The Google NGram file from which to initialize the n-gram corpus

        """
        with c_open(corpus_file, 'r', encoding='utf-8') as gng:
            for line in gng:
                line = line.rstrip().split('\t')
                words = line[0].split()

                self._add_to_ngcorpus(self.ngcorpus, words, int(line[2]))