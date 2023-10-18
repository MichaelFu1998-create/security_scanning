def get(self, id, **kwargs):
        """
        Get single unit of collection
        """
        return (super(MutableCollection, self).get((id,), **kwargs)
                .get(self.singular, None))