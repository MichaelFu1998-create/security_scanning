def read(self, filename=None):
        """Read and parse mdp file *filename*."""
        self._init_filename(filename)

        def BLANK(i):
            return "B{0:04d}".format(i)
        def COMMENT(i):
            return "C{0:04d}".format(i)

        data = odict()
        iblank = icomment = 0
        with open(self.real_filename) as mdp:
            for line in mdp:
                line = line.strip()
                if len(line) == 0:
                    iblank += 1
                    data[BLANK(iblank)] = ''
                    continue
                m = self.COMMENT.match(line)
                if m:
                    icomment += 1
                    data[COMMENT(icomment)] = m.group('value')
                    continue
                # parameter
                m = self.PARAMETER.match(line)
                if m:
                    # check for comments after parameter?? -- currently discarded
                    parameter = m.group('parameter')
                    value =  self._transform(m.group('value'))
                    data[parameter] = value
                else:
                    errmsg = '{filename!r}: unknown line in mdp file, {line!r}'.format(**vars())
                    self.logger.error(errmsg)
                    raise ParseError(errmsg)

        super(MDP,self).update(data)