def replace_bases(self, old, new):
        '''Replaces all occurrences of 'old' with 'new' '''
        self.seq = self.seq.replace(old, new)