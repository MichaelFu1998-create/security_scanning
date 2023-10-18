def list(self, root=False, **kwargs):
        """Return a list of groups.

        =====API DOCS=====
        Retrieve a list of groups.

        :param root: Flag that if set, only root groups of a specific inventory will be listed.
        :type root: bool
        :param parent: Primary key or name of the group whose child groups will be listed.
        :type parent: str
        :param all_pages: Flag that if set, collect all pages of content from the API when returning results.
        :type all_pages: bool
        :param page: The page to show. Ignored if all_pages is set.
        :type page: int
        :param query: Contains 2-tuples used as query parameters to filter resulting resource objects.
        :type query: list
        :param `**kwargs`: Keyword arguments list of available fields used for searching resource objects.
        :returns: A JSON object containing details of all resource objects returned by Tower backend.
        :rtype: dict
        :raises tower_cli.exceptions.UsageError: When ``root`` flag is on and ``inventory`` is not present in
                                                 ``**kwargs``.

        =====API DOCS=====
        """
        # Option to list children of a parent group
        if kwargs.get('parent', None):
            self.set_child_endpoint(parent=kwargs['parent'], inventory=kwargs.get('inventory', None))
            kwargs.pop('parent')
        # Sanity check: If we got `--root` and no inventory, that's an error.
        if root and not kwargs.get('inventory', None):
            raise exc.UsageError('The --root option requires specifying an inventory also.')
        # If we are tasked with getting root groups, do that.
        if root:
            inventory_id = kwargs['inventory']
            r = client.get('/inventories/%d/root_groups/' % inventory_id)
            return r.json()
        # Return the superclass implementation.
        return super(Resource, self).list(**kwargs)