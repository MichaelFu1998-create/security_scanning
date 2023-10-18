def delete_roles(apps, schema_editor):
    """Delete the enterprise roles."""
    SystemWideEnterpriseRole = apps.get_model('enterprise', 'SystemWideEnterpriseRole')
    SystemWideEnterpriseRole.objects.filter(
        name__in=[ENTERPRISE_ADMIN_ROLE, ENTERPRISE_LEARNER_ROLE]
    ).delete()