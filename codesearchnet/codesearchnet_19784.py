def _print(self, line=''):
        """Append line to internal list. 
        Uses self.tabs to format indents.
        
        Keyword arguments:
        line -- line to append
        """
        self.lines.append('{}{}'.format('\t'*self.tabs , line))