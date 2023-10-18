def import_parms(self, args):
        """Import external dict to internal dict"""

        for key, val in args.items():
            self.set_parm(key, val)