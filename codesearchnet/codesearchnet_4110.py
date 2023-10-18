def _load_rule_file(self, filename):
        """Import the given rule file"""
        if not (os.path.exists(filename)):
            sys.stderr.write("rflint: %s: No such file or directory\n" % filename)
            return
        try:
            basename = os.path.basename(filename)
            (name, ext) = os.path.splitext(basename)
            imp.load_source(name, filename)
        except Exception as e:
            sys.stderr.write("rflint: %s: exception while loading: %s\n" % (filename, str(e)))