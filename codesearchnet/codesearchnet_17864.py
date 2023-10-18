def resolve_admin_type(admin):
    """Determine admin type."""
    if admin is current_user or isinstance(admin, UserMixin):
        return 'User'
    else:
        return admin.__class__.__name__