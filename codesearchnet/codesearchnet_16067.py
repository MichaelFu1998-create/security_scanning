def replace_interval(self, start, end, new):
        '''Replaces the sequence from start to end with the sequence "new"'''
        if start > end or start > len(self) - 1 or end > len(self) - 1:
            raise Error('Error replacing bases ' + str(start) + '-' + str(end) + ' in sequence ' + self.id)

        self.seq = self.seq[0:start] + new + self.seq[end + 1:]