def _trace_summary(self):
        """
        Summarizes the trace of values used to update the DynamicArgs
        and the arguments subsequently returned. May be used to
        implement the summary method.
        """
        for (i, (val, args)) in enumerate(self.trace):
            if args is StopIteration:
                info = "Terminated"
            else:
                pprint = ','.join('{' + ','.join('%s=%r' % (k,v)
                         for (k,v) in arg.items()) + '}' for arg in args)
                info = ("exploring arguments [%s]" % pprint )

            if i == 0: print("Step %d: Initially %s." % (i, info))
            else:      print("Step %d: %s after receiving input(s) %s." % (i, info.capitalize(), val))