def fact(self, name):
        """Get a single fact from this node."""
        facts = self.facts(name=name)
        return next(fact for fact in facts)