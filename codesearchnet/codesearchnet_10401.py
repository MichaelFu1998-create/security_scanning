def read(self, filename=None):
        """Read and parse index file *filename*."""
        self._init_filename(filename)

        data = odict()
        with open(self.real_filename) as ndx:
            current_section = None
            for line in ndx:
                line = line.strip()
                if len(line) == 0:
                    continue
                m = self.SECTION.match(line)
                if m:
                    current_section = m.group('name')
                    data[current_section] = []  # can fail if name not legal python key
                    continue
                if current_section is not None:
                    data[current_section].extend(map(int, line.split()))

        super(NDX,self).update(odict([(name, self._transform(atomnumbers))
                                     for name, atomnumbers in data.items()]))