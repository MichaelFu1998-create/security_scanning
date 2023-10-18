def list_env(self, key=None):
        """
        Displays a list of environment key/value pairs.
        """
        for k, v in sorted(self.genv.items(), key=lambda o: o[0]):
            if key and k != key:
                continue
            print('%s ' % (k,))
            pprint(v, indent=4)