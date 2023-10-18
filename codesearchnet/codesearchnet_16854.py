def patch(self, *args, **kwargs):
        """Patch only drafts.

        Status required: ``'draft'``.

        Meta information inside `_deposit` are preserved.
        """
        return super(Deposit, self).patch(*args, **kwargs)