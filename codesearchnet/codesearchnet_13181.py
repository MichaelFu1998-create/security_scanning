def get_clan(self):
        """(a)sync function to return clan."""
        try:
            return self.client.get_clan(self.clan.tag)
        except AttributeError:
            try:
                return self.client.get_clan(self.tag)
            except AttributeError:
                raise ValueError('This player does not have a clan.')