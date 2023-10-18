def get(cls, group, admin):
        """Get specific GroupAdmin object."""
        try:
            ga = cls.query.filter_by(
                group=group, admin_id=admin.get_id(),
                admin_type=resolve_admin_type(admin)).one()
            return ga
        except Exception:
            return None