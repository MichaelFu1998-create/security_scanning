def post_parse(self):
        """ Post parse cycle. nodejs version allows calls to mixins
        not yet defined or known to the parser. We defer all calls
        to mixins until after first cycle when all names are known.
        """
        if self.result:
            out = []
            for pu in self.result:
                try:
                    out.append(pu.parse(self.scope))
                except SyntaxError as e:
                    self.handle_error(e, 0)
            self.result = list(utility.flatten(out))