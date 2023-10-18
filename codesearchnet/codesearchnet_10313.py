def _process_command(self, command, name=None):
        """Process ``make_ndx`` command and  return name and temp index file."""

        self._command_counter += 1
        if name is None:
            name = "CMD{0:03d}".format(self._command_counter)

        # Need to build it with two make_ndx calls because I cannot reliably
        # name the new group without knowing its number.
        try:
            fd, tmp_ndx = tempfile.mkstemp(suffix='.ndx', prefix='tmp_'+name+'__')
            cmd = [command, '', 'q']   # empty command '' necessary to get list
            # This sometimes fails with 'OSError: Broken Pipe' --- hard to debug
            rc,out,err = self.make_ndx(o=tmp_ndx, input=cmd)
            self.check_output(out, "No atoms found for selection {command!r}.".format(**vars()), err=err)
            # For debugging, look at out and err or set stdout=True, stderr=True
            # TODO: check '  0 r_300_&_ALA_&_O     :     1 atoms' has at least 1 atom
            ##print "DEBUG: _process_command()"
            ##print out
            groups = parse_ndxlist(out)
            last = groups[-1]
            # reduce and name this group
            fd, ndx = tempfile.mkstemp(suffix='.ndx', prefix=name+'__')
            name_cmd = ["keep {0:d}".format(last['nr']),
                        "name 0 {0!s}".format(name), 'q']
            rc,out,err = self.make_ndx(n=tmp_ndx, o=ndx, input=name_cmd)
        finally:
            utilities.unlink_gmx(tmp_ndx)

        return name, ndx