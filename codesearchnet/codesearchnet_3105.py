def match(self, string, pos):
        '''string is of course a py string'''
        return self.pat.match(string, int(pos))