def output(self, to=None, *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        for blok in self:
            blok.output(to, *args, **kwargs)
        return self