def modify(self, pk=None, create_on_missing=False, **kwargs):
        """Modify an already existing.

        To edit the project's organizations, see help for organizations.

        Fields in the resource's `identity` tuple can be used in lieu of a
        primary key for a lookup; in such a case, only other fields are
        written.

        To modify unique fields, you must use the primary key for the lookup.

        =====API DOCS=====
        Modify an already existing project.

        :param pk: Primary key of the resource to be modified.
        :type pk: int
        :param create_on_missing: Flag that if set, a new object is created if ``pk`` is not set and objects
                                  matching the appropriate unique criteria is not found.
        :type create_on_missing: bool
        :param `**kwargs`: Keyword arguments which, all together, will be used as PATCH body to modify the
                           resource object. if ``pk`` is not set, key-value pairs of ``**kwargs`` which are
                           also in resource's identity will be used to lookup existing reosource.
        :returns: A dictionary combining the JSON output of the modified resource, as well as two extra fields:
                  "changed", a flag indicating if the resource is successfully updated; "id", an integer which
                  is the primary key of the updated object.
        :rtype: dict

        =====API DOCS=====
        """
        # Associated with issue #52, the organization can't be modified
        #    with the 'modify' command. This would create confusion about
        #    whether its flag is an identifier versus a field to modify.
        if 'job_timeout' in kwargs and 'timeout' not in kwargs:
            kwargs['timeout'] = kwargs.pop('job_timeout')
        return super(Resource, self).write(
            pk, create_on_missing=create_on_missing,
            force_on_exists=True, **kwargs
        )