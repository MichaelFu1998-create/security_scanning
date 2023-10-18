def print_tree(self, maxresults=100, maxdepth=None):
        """Walk the object tree, pretty-printing each branch."""
        self.ignore_caller()
        for trail in self.walk(maxresults, maxdepth):
            print(trail)
        if self.stops:
            print("%s paths stopped because max depth reached" % self.stops)