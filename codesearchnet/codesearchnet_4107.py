def list_rules(self):
        """Print a list of all rules"""
        for rule in sorted(self.all_rules, key=lambda rule: rule.name):
            print(rule)
            if self.args.verbose:
                for line in rule.doc.split("\n"):
                    print("    ", line)