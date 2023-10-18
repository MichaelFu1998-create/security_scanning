def _parse_names(self):
        """ parse sample names from the sequence file"""
        self.samples = []
        with iter(open(self.files.data, 'r')) as infile:
            infile.next().strip().split()
            while 1:
                try:
                    self.samples.append(infile.next().split()[0])
                except StopIteration:
                    break