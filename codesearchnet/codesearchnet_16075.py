def trim(self, start, end):
        '''Removes first 'start'/'end' bases off the start/end of the sequence'''
        self.seq = self.seq[start:len(self.seq) - end]