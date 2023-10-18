def trim(self, start, end):
        '''Removes first 'start'/'end' bases off the start/end of the sequence'''
        super().trim(start, end)
        self.qual = self.qual[start:len(self.qual) - end]