def knock_out(self):
        """Knockout gene by marking it as non-functional and setting all
        associated reactions bounds to zero.

        The change is reverted upon exit if executed within the model as
        context.
        """
        self.functional = False
        for reaction in self.reactions:
            if not reaction.functional:
                reaction.bounds = (0, 0)