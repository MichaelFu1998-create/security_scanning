def data_endpoint(cls, in_data, ignore=[]):
        """
        Converts a set of CLI input arguments, `in_data`, into
        request data and an endpoint that can be used to look
        up a role or list of roles.

        Also changes the format of `type` in data to what the server
        expects for the role model, as it exists in the database.
        """
        obj, obj_type, res, res_type = cls.obj_res(in_data, fail_on=[])
        data = {}
        if 'obj' in ignore:
            obj = None
        if 'res' in ignore:
            res = None
        # Input fields are not actually present on role model, and all have
        # to be managed as individual special-cases
        if obj and obj_type == 'user':
            data['members__in'] = obj
        if obj and obj_type == 'team':
            endpoint = '%s/%s/roles/' % (grammar.pluralize(obj_type), obj)
            if res is not None:
                # For teams, this is the best lookup we can do
                #  without making the additional request for its member_role
                data['object_id'] = res
        elif res:
            endpoint = '%s/%s/object_roles/' % (grammar.pluralize(res_type), res)
        else:
            endpoint = '/roles/'
        if in_data.get('type', False):
            data['role_field'] = '%s_role' % in_data['type'].lower()
        # Add back fields unrelated to role lookup, such as all_pages
        for key, value in in_data.items():
            if key not in RESOURCE_FIELDS and key not in ['type', 'user', 'team']:
                data[key] = value
        return data, endpoint