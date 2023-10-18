def files(self):
        """List of Files inside the deposit.

        Add validation on ``sort_by`` method: if, at the time of files access,
        the record is not a ``'draft'`` then a
        :exc:`invenio_pidstore.errors.PIDInvalidAction` is rised.
        """
        files_ = super(Deposit, self).files

        if files_:
            sort_by_ = files_.sort_by

            def sort_by(*args, **kwargs):
                """Only in draft state."""
                if 'draft' != self.status:
                    raise PIDInvalidAction()
                return sort_by_(*args, **kwargs)

            files_.sort_by = sort_by

        return files_