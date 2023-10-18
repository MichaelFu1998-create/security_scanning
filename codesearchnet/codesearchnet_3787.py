def delete(self, pk=None, fail_on_missing=False, **kwargs):
        """Remove the given notification template.

        Note here configuration-related fields like
        'notification_configuration' and 'channels' will not be
        used even provided.

        If `fail_on_missing` is True, then the object's not being found is
        considered a failure; otherwise, a success with no change is reported.

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
        self._separate(kwargs)
        return super(Resource, self).\
            delete(pk=pk, fail_on_missing=fail_on_missing, **kwargs)