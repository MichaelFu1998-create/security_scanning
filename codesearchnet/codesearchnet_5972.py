def go(function_expr, **kwargs):
        """
        CloudAux.go(
            'list_aliases',
            **{
                'account_number': '000000000000',
                'assume_role': 'role_name',
                'session_name': 'cloudaux',
                'region': 'us-east-1',
                'tech': 'kms',
                'service_type': 'client'
            })

        CloudAux.go(
            'kms.client.list_aliases',
            **{
                'account_number': '000000000000',
                'assume_role': 'role_name',
                'session_name': 'cloudaux',
                'region': 'us-east-1'
            })
        """
        if '.' in function_expr:
            tech, service_type, function_name = function_expr.split('.')
        else:
            tech = kwargs.pop('tech')
            service_type = kwargs.get('service_type')
            function_name = function_expr

        @sts_conn(tech, service_type=service_type)
        def wrapped_method(function_name, **nargs):
            service_type = nargs.pop(nargs.pop('service_type', 'client'))
            return getattr(service_type, function_name)(**nargs)

        return wrapped_method(function_name, **kwargs)