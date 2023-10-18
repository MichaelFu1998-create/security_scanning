def output(self, to=None, formatted=False, indent=0, indentation='  ', *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        if formatted and self.blox:
            self.blox[0].output(to=to, formatted=True, indent=indent, indentation=indentation, *args, **kwargs)
            for blok in self.blox[1:]:
                to.write('\n')
                to.write(indent * indentation)
                blok.output(to=to, formatted=True, indent=indent, indentation=indentation, *args, **kwargs)
            if not indent:
                to.write('\n')
        else:
            for blok in self.blox:
                blok.output(to=to, *args, **kwargs)

        return self