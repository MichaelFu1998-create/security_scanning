def copy(self, pk=None, new_name=None, **kwargs):
        """Copy an object.

        Only the ID is used for the lookup. All provided fields are used to override the old data from the
        copied resource.

        =====API DOCS=====
        Copy an object.

        :param pk: Primary key of the resource object to be copied
        :param new_name: The new name to give the resource if deep copying via the API
        :type pk: int
        :param `**kwargs`: Keyword arguments of fields whose given value will override the original value.
        :returns: loaded JSON of the copied new resource object.
        :rtype: dict

        =====API DOCS=====
        """
        orig = self.read(pk, fail_on_no_results=True, fail_on_multiple_results=True)
        orig = orig['results'][0]
        # Remove default values (anything where the value is None).
        self._pop_none(kwargs)

        newresource = copy(orig)
        newresource.pop('id')
        basename = newresource['name'].split('@', 1)[0].strip()

        # Modify data to fit the call pattern of the tower-cli method
        for field in self.fields:
            if field.multiple and field.name in newresource:
                newresource[field.name] = (newresource.get(field.name),)

        if new_name is None:
            # copy client-side, the old mechanism
            newresource['name'] = "%s @ %s" % (basename, time.strftime('%X'))
            newresource.update(kwargs)

            return self.write(create_on_missing=True, fail_on_found=True,
                              **newresource)
        else:
            # copy server-side, the new mechanism
            if kwargs:
                raise exc.TowerCLIError('Cannot override {} and also use --new-name.'.format(kwargs.keys()))
            copy_endpoint = '{}/{}/copy/'.format(self.endpoint.strip('/'), pk)
            return client.post(copy_endpoint, data={'name': new_name}).json()