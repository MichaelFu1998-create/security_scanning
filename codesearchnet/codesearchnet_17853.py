def users():
    """Load default users and groups."""
    from invenio_groups.models import Group, Membership, \
        PrivacyPolicy, SubscriptionPolicy

    admin = accounts.datastore.create_user(
        email='admin@inveniosoftware.org',
        password=encrypt_password('123456'),
        active=True,
    )
    reader = accounts.datastore.create_user(
        email='reader@inveniosoftware.org',
        password=encrypt_password('123456'),
        active=True,
    )

    admins = Group.create(name='admins', admins=[admin])
    for i in range(10):
        Group.create(name='group-{0}'.format(i), admins=[admin])
    Membership.create(admins, reader)
    db.session.commit()