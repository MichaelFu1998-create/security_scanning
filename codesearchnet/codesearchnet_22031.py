def create_admin(username='admin', email='admin@admin.com', password='admin'):
    """Create and save an admin user.

    :param username:
        Admin account's username.  Defaults to 'admin'
    :param email:
        Admin account's email address.  Defaults to 'admin@admin.com'
    :param password:
        Admin account's password.  Defaults to 'admin'
    :returns:
        Django user with staff and superuser privileges
    """
    admin = User.objects.create_user(username, email, password)
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    return admin