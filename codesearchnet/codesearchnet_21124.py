def output(self, to=None, formatted=False, indent=0, indentation='  ', *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        if formatted:
            to.write(self.start_tag)
            to.write('\n')
            if not self.tag_self_closes:
                for blok in self.blox:
                    to.write(indentation * (indent + 1))
                    blok.output(to=to, indent=indent + 1, formatted=True, indentation=indentation, *args, **kwargs)
                    to.write('\n')

            to.write(indentation * indent)
            to.write(self.end_tag)
            if not indentation:
                to.write('\n')
        else:
            to.write(self.start_tag)
            if not self.tag_self_closes:
                for blok in self.blox:
                    blok.output(to=to, *args, **kwargs)
            to.write(self.end_tag)