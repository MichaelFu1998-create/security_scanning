def convert(self, value, param, ctx):
        """Return the appropriate integer value. If a non-integer is
        provided, attempt a name-based lookup and return the primary key.
        """
        resource = tower_cli.get_resource(self.resource_name)

        # Ensure that None is passed through without trying to
        # do anything.
        if value is None:
            return None

        # If we were already given an integer, do nothing.
        # This ensures that the convert method is idempotent.
        if isinstance(value, int):
            return value

        # Do we have a string that contains only digits?
        # If so, then convert it to an integer and return it.
        if re.match(r'^[\d]+$', value):
            return int(value)

        # Special case to allow disassociations
        if value == 'null':
            return value

        # Okay, we have a string. Try to do a name-based lookup on the
        # resource, and return back the ID that we get from that.
        #
        # This has the chance of erroring out, which is fine.
        try:
            debug.log('The %s field is given as a name; '
                      'looking it up.' % param.name, header='details')
            lookup_data = {resource.identity[-1]: value}
            rel = resource.get(**lookup_data)
        except exc.MultipleResults:
            raise exc.MultipleRelatedError(
                'Cannot look up {0} exclusively by name, because multiple {0} '
                'objects exist with that name.\n'
                'Please send an ID. You can get the ID for the {0} you want '
                'with:\n'
                '  tower-cli {0} list --name "{1}"'.format(self.resource_name,
                                                           value),
            )
        except exc.TowerCLIError as ex:
            raise exc.RelatedError('Could not get %s. %s' %
                                   (self.resource_name, str(ex)))

        # Done! Return the ID.
        return rel['id']