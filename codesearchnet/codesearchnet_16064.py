def is_all_Ns(self, start=0, end=None):
        '''Returns true if the sequence is all Ns (upper or lower case)'''
        if end is not None:
            if start > end:
                raise Error('Error in is_all_Ns. Start coord must be <= end coord')
            end += 1
        else:
            end = len(self)

        if len(self) == 0:
            return False
        else:
            return re.search('[^Nn]', self.seq[start:end]) is None