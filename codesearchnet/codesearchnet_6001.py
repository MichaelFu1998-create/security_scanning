def get_iam_policy(client=None, **kwargs):
    """
    service_account='string'
    """
    service_account=kwargs.pop('service_account')
    resp = client.projects().serviceAccounts().getIamPolicy(
        resource=service_account).execute()
    # TODO(supertom): err handling, check if 'bindings' is correct
    if 'bindings' in resp:
        return resp['bindings']
    else:
        return None