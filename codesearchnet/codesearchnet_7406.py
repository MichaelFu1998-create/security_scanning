def everything(self, query):
        """
        Retrieve all items in the library for a particular query
        This method will override the 'limit' parameter if it's been set
        """
        try:
            items = []
            items.extend(query)
            while self.links.get("next"):
                items.extend(self.follow())
        except TypeError:
            # we have a bibliography object ughh
            items = copy.deepcopy(query)
            while self.links.get("next"):
                items.entries.extend(self.follow().entries)
        return items