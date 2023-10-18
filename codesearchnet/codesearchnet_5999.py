def get_serviceaccount(client=None, **kwargs):
    """
    service_account='string'
    """
    service_account=kwargs.pop('service_account')
    resp = client.projects().serviceAccounts().get(
        name=service_account).execute()
    return resp