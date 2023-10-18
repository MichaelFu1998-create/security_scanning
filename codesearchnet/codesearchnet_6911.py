def load_included_indentifiers(self, file_name):
        '''Loads a file with newline-separated integers representing which 
        chemical should be kept in memory; ones not included are ignored.
        '''
        self.restrict_identifiers = True
        included_identifiers = set()       
        with open(file_name) as f:
            [included_identifiers.add(int(line)) for line in f]
        self.included_identifiers = included_identifiers