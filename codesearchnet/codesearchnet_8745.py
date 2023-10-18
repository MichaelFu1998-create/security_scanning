def delete_enterprise_learner_role_assignment(sender, instance, **kwargs):     # pylint: disable=unused-argument
    """
    Delete the associated enterprise learner role assignment record when deleting an EnterpriseCustomerUser record.
    """
    if instance.user:
        enterprise_learner_role, __ = SystemWideEnterpriseRole.objects.get_or_create(name=ENTERPRISE_LEARNER_ROLE)
        try:
            SystemWideEnterpriseUserRoleAssignment.objects.get(
                user=instance.user,
                role=enterprise_learner_role
            ).delete()
        except SystemWideEnterpriseUserRoleAssignment.DoesNotExist:
            # Do nothing if no role assignment is present for the enterprise customer user.
            pass