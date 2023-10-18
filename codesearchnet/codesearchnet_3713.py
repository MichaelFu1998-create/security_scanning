def delete(self, pk=None, fail_on_missing=False, **kwargs):
        """Remove the given object.

        If `fail_on_missing` is True, then the object's not being found is considered a failure; otherwise,
        a success with no change is reported.

        =====API DOCS=====
        Remove the given object.

        :param pk: Primary key of the resource to be deleted.
        :type pk: int
        :param fail_on_missing: Flag that if set, the object's not being found is considered a failure; otherwise,
                                a success with no change is reported.
        :type fail_on_missing: bool
        :param `**kwargs`: Keyword arguments used to look up resource object to delete if ``pk`` is not provided.
        :returns: dictionary of only one field "changed", which is a flag indicating whether the specified resource
                  is successfully deleted.
        :rtype: dict

        =====API DOCS=====
        """
        # If we weren't given a primary key, determine which record we're deleting.
        if not pk:
            existing_data = self._lookup(fail_on_missing=fail_on_missing, **kwargs)
            if not existing_data:
                return {'changed': False}
            pk = existing_data['id']

        # Attempt to delete the record. If it turns out the record doesn't exist, handle the 404 appropriately
        # (this is an okay response if `fail_on_missing` is False).
        url = '%s%s/' % (self.endpoint, pk)
        debug.log('DELETE %s' % url, fg='blue', bold=True)
        try:
            client.delete(url)
            return {'changed': True}
        except exc.NotFound:
            if fail_on_missing:
                raise
            return {'changed': False}