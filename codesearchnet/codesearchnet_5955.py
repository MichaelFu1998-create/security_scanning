def gcp_conn(service, service_type='client', future_expiration_minutes=15):
    """
    service_type: not currently used.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Import here to avoid circular import issue
            from cloudaux.gcp.auth import get_client
            (conn_args, kwargs) = get_creds_from_kwargs(kwargs)
            client_details, client = get_client(
                service, service_type=service_type,
                future_expiration_minutes=15, **conn_args)
            if client_details:
                kwargs = rewrite_kwargs(client_details['client_type'], kwargs,
                                    client_details['module_name'])
            kwargs['client'] = client
            return f(*args, **kwargs)

        return decorated_function

    return decorator