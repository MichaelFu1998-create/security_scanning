def obj_res(data, fail_on=['type', 'obj', 'res']):
        """
        Given some CLI input data,
        Returns the following and their types:
        obj - the role grantee
        res - the resource that the role applies to
        """
        errors = []
        if not data.get('type', None) and 'type' in fail_on:
            errors += ['You must provide a role type to use this command.']

        # Find the grantee, and remove them from resource_list
        obj = None
        obj_type = None
        for fd in ACTOR_FIELDS:
            if data.get(fd, False):
                if not obj:
                    obj = data[fd]
                    obj_type = fd
                else:
                    errors += ['You can not give a role to a user '
                               'and team at the same time.']
                    break
        if not obj and 'obj' in fail_on:
            errors += ['You must specify either user or '
                       'team to use this command.']

        # Out of the resource list, pick out available valid resource field
        res = None
        res_type = None
        for fd in RESOURCE_FIELDS:
            if data.get(fd, False):
                if not res:
                    res = data[fd]
                    res_type = fd
                    if res_type == 'target_team':
                        res_type = 'team'
                else:
                    errors += ['You can only give a role to one '
                               'type of resource at a time.']
                    break
        if not res and 'res' in fail_on:
            errors += ['You must specify a target resource '
                       'to use this command.']

        if errors:
            raise exc.UsageError("\n".join(errors))
        return obj, obj_type, res, res_type