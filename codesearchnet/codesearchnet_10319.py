def rp(self, *args):
        """Return canonical path to file under *dirname* with components *args*

         If *args* form an absolute path then just return it as the absolute path.
         """
        try:
            p = os.path.join(*args)
            if os.path.isabs(p):
                return p
        except TypeError:
            pass
        return utilities.realpath(self.dirname, *args)