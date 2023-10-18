def iterfollow(self):
        """ Generator for self.follow()
        """
        # use same criterion as self.follow()
        if self.links is None:
            return
        if self.links.get("next"):
            yield self.follow()
        else:
            raise StopIteration