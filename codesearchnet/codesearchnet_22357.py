def pre(self, command, output_dir, vars):
        """
        Called before template is applied.
        """
        # import pdb;pdb.set_trace()
        vars['license_name'] = 'Apache'
        vars['year'] = time.strftime('%Y', time.localtime())