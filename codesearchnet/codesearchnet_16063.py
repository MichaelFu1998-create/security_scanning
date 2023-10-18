def strip_illumina_suffix(self):
        '''Removes any trailing /1 or /2 off the end of the name'''
        if self.id.endswith('/1') or self.id.endswith('/2'):
            self.id = self.id[:-2]