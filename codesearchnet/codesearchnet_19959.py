def review_args(self, obj, show_repr=False, heading='Arguments'):
        """
        Reviews the given argument specification. Can review the
        meta-arguments (launch_args) or the arguments themselves.
        """
        args = obj.args if isinstance(obj, Launcher) else obj
        print('\n%s\n' % self.summary_heading(heading))
        args.summary()
        if show_repr: print("\n%s\n" % args)
        response = self.input_options(['y', 'N','quit'],
                '\nShow available argument specifier entries?', default='n')
        if response == 'quit': return False
        if response == 'y':  args.show()
        print('')
        return True