def query_by_admin(cls, admin):
        """Get all groups for for a specific admin."""
        return cls.query.filter_by(
            admin_type=resolve_admin_type(admin), admin_id=admin.get_id())