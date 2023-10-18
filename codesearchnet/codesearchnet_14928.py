def find_libname(self, name):
        """Try to infer the correct library name."""
        names = ["{}.lib", "lib{}.lib", "{}lib.lib"]
        names = [n.format(name) for n in names]
        dirs = self.get_library_dirs()
        for d in dirs:
            for n in names:
                if exists(join(d, n)):
                    return n[:-4]
        msg = "Could not find the {} library.".format(name)
        raise ValueError(msg)