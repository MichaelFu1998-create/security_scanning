def convert(self, value, param, ctx):
        """Match against the appropriate choice value using the superclass
        implementation, and then return the actual choice.
        """
        choice = super(MappedChoice, self).convert(value, param, ctx)
        ix = self.choices.index(choice)
        return self.actual_choices[ix]