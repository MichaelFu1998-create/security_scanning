def write(self, filename=None, skipempty=False):
        """Write mdp file to *filename*.

        :Keywords:
           *filename*
               output mdp file; default is the filename the mdp
               was read from
           *skipempty* : boolean
               ``True`` removes any parameter lines from output that
               contain empty values [``False``]

        .. Note:: Overwrites the file that the mdp was read from if no
                  *filename* supplied.
        """

        with open(self.filename(filename, ext='mdp'), 'w') as mdp:
            for k,v in self.items():
                if k[0] == 'B':        # blank line
                    mdp.write("\n")
                elif k[0] == 'C':      # comment
                    mdp.write("; {v!s}\n".format(**vars()))
                else:                  # parameter = value
                    if skipempty and (v == '' or v is None):
                        continue
                    if isinstance(v, six.string_types) or not hasattr(v, '__iter__'):
                        mdp.write("{k!s} = {v!s}\n".format(**vars()))
                    else:
                         mdp.write("{} = {}\n".format(k,' '.join(map(str, v))))