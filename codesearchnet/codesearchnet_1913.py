def dotted_name(self, idents):
        """dotted_name: NAME ('.' NAME)*"""
        return idents[0].loc.join(idents[-1].loc), \
               ".".join(list(map(lambda x: x.value, idents)))