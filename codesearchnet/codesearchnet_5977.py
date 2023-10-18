def get_role_managed_policy_documents(role, client=None, **kwargs):
    """Retrieve the currently active policy version document for every managed policy that is attached to the role."""
    policies = get_role_managed_policies(role, force_client=client)

    policy_names = (policy['name'] for policy in policies)
    delayed_gmpd_calls = (delayed(get_managed_policy_document)(policy['arn'], force_client=client) for policy
                          in policies)
    policy_documents = Parallel(n_jobs=20, backend="threading")(delayed_gmpd_calls)

    return dict(zip(policy_names, policy_documents))