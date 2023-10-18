def clear(self, *args, **kwargs):
        """Clear only drafts.

        Status required: ``'draft'``.

        Meta information inside `_deposit` are preserved.
        """
        super(Deposit, self).clear(*args, **kwargs)