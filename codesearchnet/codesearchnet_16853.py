def update(self, *args, **kwargs):
        """Update only drafts.

        Status required: ``'draft'``.

        Meta information inside `_deposit` are preserved.
        """
        super(Deposit, self).update(*args, **kwargs)