def print_parents(self):
        """Print parents' names and epithets."""
        if self.gender == female:
            title = 'Daughter'
        elif self.gender == male:
            title = 'Son'
        else:
            title = 'Child'

        p1 = self.parents[0]
        p2 = self.parents[1]

        template = '%s of %s, the %s, and %s, the %s.'

        print(template % (title, p1.name, p1.epithet, p2.name, p2.epithet))