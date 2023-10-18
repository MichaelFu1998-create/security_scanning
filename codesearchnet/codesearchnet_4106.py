def run(self, args):
        """Parse command line arguments, and run rflint"""

        self.args = self.parse_and_process_args(args)

        if self.args.version:
            print(__version__)
            return 0
            
        if self.args.rulefile:
            for filename in self.args.rulefile:
                self._load_rule_file(filename)

        if self.args.list:
            self.list_rules()
            return 0
        
        if self.args.describe:
            self._describe_rules(self.args.args)
            return 0

        self.counts = { ERROR: 0, WARNING: 0, "other": 0}
            
        for filename in self.args.args:
            if not (os.path.exists(filename)):
                sys.stderr.write("rflint: %s: No such file or directory\n" % filename)
                continue
            if os.path.isdir(filename):
                self._process_folder(filename)
            else:
                self._process_file(filename)

        if self.counts[ERROR] > 0:
            return self.counts[ERROR] if self.counts[ERROR] < 254 else 255

        return 0