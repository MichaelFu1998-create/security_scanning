def check_mro(self, bases):
        """Check if C3 MRO is possible with given bases"""

        try:
            self.add_node("temp")
            for base in bases:
                nx.DiGraph.add_edge(self, base, "temp")
            result = self.get_mro("temp")[1:]

        finally:
            self.remove_node("temp")

        return result