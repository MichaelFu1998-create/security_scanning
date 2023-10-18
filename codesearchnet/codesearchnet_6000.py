def get_serviceaccount_keys(client=None, **kwargs):
    """
    service_account='string'
    """
    service_account=kwargs.pop('service_account')
    kwargs['name'] = service_account
    return service_list(client.projects().serviceAccounts().keys(),
                        key_name='keys', **kwargs)