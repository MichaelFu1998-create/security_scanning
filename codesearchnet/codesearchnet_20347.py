def rename(self, id, name):
        """
        Change the name of this domain record

        Parameters
        ----------
        id: int
            domain record id
        name: str
            new name of record
        """
        return super(DomainRecords, self).update(id, name=name)[self.singular]