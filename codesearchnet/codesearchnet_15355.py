def includeme(config):
    """Configuration include fuction for this module"""
    api_key_authn_policy = APIKeyAuthenticationPolicy()
    config.include('openstax_accounts')
    openstax_authn_policy = config.registry.getUtility(
        IOpenstaxAccountsAuthenticationPolicy)

    # Set up api & user authentication policies.
    policies = [api_key_authn_policy, openstax_authn_policy]
    authn_policy = MultiAuthenticationPolicy(policies)
    config.set_authentication_policy(authn_policy)

    # Set up the authorization policy.
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)