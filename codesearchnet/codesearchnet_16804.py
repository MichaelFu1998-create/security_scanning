def admin_permission_factory():
    """Factory for creating a permission for an admin `deposit-admin-access`.

    If `invenio-access` module is installed, it returns a
    :class:`invenio_access.permissions.DynamicPermission` object.
    Otherwise, it returns a :class:`flask_principal.Permission` object.

    :returns: Permission instance.
    """
    try:
        pkg_resources.get_distribution('invenio-access')
        from invenio_access.permissions import DynamicPermission as Permission
    except pkg_resources.DistributionNotFound:
        from flask_principal import Permission

    return Permission(action_admin_access)