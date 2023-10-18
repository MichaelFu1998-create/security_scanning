def check_output(self, make_ndx_output, message=None, err=None):
        """Simple tests to flag problems with a ``make_ndx`` run."""
        if message is None:
            message = ""
        else:
            message = '\n' + message
        def format(output, w=60):
            hrule = "====[ GromacsError (diagnostic output) ]".ljust(w,"=")
            return hrule + '\n' + str(output) + hrule

        rc = True
        if self._is_empty_group(make_ndx_output):
            warnings.warn("Selection produced empty group.{message!s}".format(**vars()), category=GromacsValueWarning)
            rc = False
        if self._has_syntax_error(make_ndx_output):
            rc = False
            out_formatted = format(make_ndx_output)
            raise GromacsError("make_ndx encountered a Syntax Error, "
                               "%(message)s\noutput:\n%(out_formatted)s" % vars())
        if make_ndx_output.strip() == "":
            rc = False
            out_formatted = format(err)
            raise GromacsError("make_ndx produced no output, "
                               "%(message)s\nerror output:\n%(out_formatted)s" % vars())
        return rc