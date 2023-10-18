def array(self, directories):
        """Return multiline string for simple array jobs over *directories*.

        .. Warning:: The string is in ``bash`` and hence the template must also
                     be ``bash`` (and *not* ``csh`` or ``sh``).
        """
        if not self.has_arrays():
            raise NotImplementedError('Not known how make array jobs for '
                                      'queuing system %(name)s' % vars(self))
        hrule = '#'+60*'-'
        lines = [
            '',
            hrule,
            '# job array:',
            self.array_flag(directories),
            hrule,
            '# directories for job tasks',
            'declare -a jobdirs']
        for i,dirname in enumerate(asiterable(directories)):
            idx = i+1   # job array indices are 1-based
            lines.append('jobdirs[{idx:d}]={dirname!r}'.format(**vars()))
        lines.extend([
                '# Switch to the current tasks directory:',
                'wdir="${{jobdirs[${{{array_variable!s}}}]}}"'.format(**vars(self)),
                'cd "$wdir" || { echo "ERROR: failed to enter $wdir."; exit 1; }',
                hrule,
                ''
                ])
        return "\n".join(lines)