def publish(self, pid=None, id_=None):
        """Publish a deposit.

        If it's the first time:

        * it calls the minter and set the following meta information inside
            the deposit:

        .. code-block:: python

            deposit['_deposit'] = {
                'type': pid_type,
                'value': pid_value,
                'revision_id': 0,
            }

        * A dump of all information inside the deposit is done.

        * A snapshot of the files is done.

        Otherwise, published the new edited version.
        In this case, if in the mainwhile someone already published a new
        version, it'll try to merge the changes with the latest version.

        .. note:: no need for indexing as it calls `self.commit()`.

        Status required: ``'draft'``.

        :param pid: Force the new pid value. (Default: ``None``)
        :param id_: Force the new uuid value as deposit id. (Default: ``None``)
        :returns: Returns itself.
        """
        pid = pid or self.pid

        if not pid.is_registered():
            raise PIDInvalidAction()

        self['_deposit']['status'] = 'published'

        if self['_deposit'].get('pid') is None:  # First publishing
            self._publish_new(id_=id_)
        else:  # Update after edit
            record = self._publish_edited()
            record.commit()
        self.commit()
        return self