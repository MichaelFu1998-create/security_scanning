def replace_interval(self, start, end, new, qual_string):
        '''Replaces the sequence from start to end with the sequence "new"'''
        if len(new) != len(qual_string):
            raise Error('Length of new seq and qual string in replace_interval() must be equal. Cannot continue')
        super().replace_interval(start, end, new)
        self.qual = self.qual[0:start] + qual_string + self.qual[end + 1:]