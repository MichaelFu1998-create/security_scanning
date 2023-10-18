def can_run_from_cli(self):
        """return True if this script can be run from the command line"""
        ret = False
        ast_tree = ast.parse(self.body, self.path)
        calls = self._find_calls(ast_tree, __name__, "exit")
        for call in calls:
            if re.search("{}\(".format(re.escape(call)), self.body):
                ret = True
                break

        return ret