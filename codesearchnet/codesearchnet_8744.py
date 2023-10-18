def assign_enterprise_learner_role(sender, instance, **kwargs):     # pylint: disable=unused-argument
    """
    Assign an enterprise learner role to EnterpriseCustomerUser whenever a new record is created.
    """
    if kwargs['created'] and instance.user:
        enterprise_learner_role, __ = SystemWideEnterpriseRole.objects.get_or_create(name=ENTERPRISE_LEARNER_ROLE)
        SystemWideEnterpriseUserRoleAssignment.objects.get_or_create(
            user=instance.user,
            role=enterprise_learner_role
        )