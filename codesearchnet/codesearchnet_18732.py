def module(self):
        """load the module so we can actually run the script's function"""
        # we have to guard this value because:
        # https://thingspython.wordpress.com/2010/09/27/another-super-wrinkle-raising-typeerror/
        if not hasattr(self, '_module'):
            if "__main__" in sys.modules:
                mod = sys.modules["__main__"]
                path = self.normalize_path(mod.__file__)
                if os.path.splitext(path) == os.path.splitext(self.path):
                    self._module = mod

                else:
                    # http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
                    self._module = imp.load_source('captain_script', self.path)
                    #self._module = imp.load_source(self.module_name, self.path)

        return self._module