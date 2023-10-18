def populate_data_sharing_consent(apps, schema_editor):
    """
    Populates the ``DataSharingConsent`` model with the ``enterprise`` application's consent data.

    Consent data from the ``enterprise`` application come from the ``EnterpriseCourseEnrollment`` model.
    """
    DataSharingConsent = apps.get_model('consent', 'DataSharingConsent')
    EnterpriseCourseEnrollment = apps.get_model('enterprise', 'EnterpriseCourseEnrollment')
    User = apps.get_model('auth', 'User')
    for enrollment in EnterpriseCourseEnrollment.objects.all():
        user = User.objects.get(pk=enrollment.enterprise_customer_user.user_id)
        data_sharing_consent, __ = DataSharingConsent.objects.get_or_create(
            username=user.username,
            enterprise_customer=enrollment.enterprise_customer_user.enterprise_customer,
            course_id=enrollment.course_id,
        )
        if enrollment.consent_granted is not None:
            data_sharing_consent.granted = enrollment.consent_granted
        else:
            # Check UDSCA instead.
            consent_state = enrollment.enterprise_customer_user.data_sharing_consent.first()
            if consent_state is not None:
                data_sharing_consent.granted = consent_state.state in ['enabled', 'external']
            else:
                data_sharing_consent.granted = False
        data_sharing_consent.save()