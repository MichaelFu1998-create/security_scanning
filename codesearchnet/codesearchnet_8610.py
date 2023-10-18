def create_switch(apps, schema_editor):
    """Create and activate the SAP_USE_ENTERPRISE_ENROLLMENT_PAGE switch if it does not already exist."""
    Switch = apps.get_model('waffle', 'Switch')
    Switch.objects.get_or_create(name='SAP_USE_ENTERPRISE_ENROLLMENT_PAGE', defaults={'active': False})