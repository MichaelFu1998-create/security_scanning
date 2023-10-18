def role_write(self, fail_on_found=False, disassociate=False, **kwargs):
        """Re-implementation of the parent `write` method specific to roles.
        Adds a grantee (user or team) to the resource's role."""

        # Get the role, using only the resource data
        data, self.endpoint = self.data_endpoint(kwargs, ignore=['obj'])
        debug.log('Checking if role exists.', header='details')
        response = self.read(pk=None, fail_on_no_results=True,
                             fail_on_multiple_results=True, **data)
        role_data = response['results'][0]
        role_id = role_data['id']

        # Role exists, change display settings to output something
        self.configure_display(role_data, kwargs, write=True)

        # Check if user/team has this role
        # Implictly, force_on_exists is false for roles
        obj, obj_type, res, res_type = self.obj_res(kwargs)
        debug.log('Checking if %s already has role.' % obj_type,
                  header='details')
        data, self.endpoint = self.data_endpoint(kwargs)
        data['content_type__model'] = res_type.replace('_', '')
        response = self.read(pk=None, fail_on_no_results=False,
                             fail_on_multiple_results=False, **data)

        msg = ''
        if response['count'] > 0 and not disassociate:
            msg = 'This %s is already a member of the role.' % obj_type
        elif response['count'] == 0 and disassociate:
            msg = 'This %s is already a non-member of the role.' % obj_type

        if msg:
            role_data['changed'] = False
            if fail_on_found:
                raise exc.NotFound(msg)
            else:
                debug.log(msg, header='DECISION')
                return role_data

        # Add or remove the user/team to the role
        debug.log('Attempting to %s the %s in this role.' % (
            'remove' if disassociate else 'add', obj_type), header='details')
        post_data = {'id': role_id}
        if disassociate:
            post_data['disassociate'] = True
        client.post('%s/%s/roles/' % (grammar.pluralize(obj_type), obj),
                    data=post_data)
        role_data['changed'] = True
        return role_data