def get_user_from_social_auth(tpa_provider, tpa_username):
    """
    Find the LMS user from the LMS model `UserSocialAuth`.

    Arguments:
        tpa_provider (third_party_auth.provider): third party auth provider object
        tpa_username (str): Username returned by the third party auth

    """
    user_social_auth = UserSocialAuth.objects.select_related('user').filter(
        user__username=tpa_username, provider=tpa_provider.backend_name
    ).first()

    return user_social_auth.user if user_social_auth else None