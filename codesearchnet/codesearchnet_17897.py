def query_admins_by_group_ids(cls, groups_ids=None):
        """Get count of admins per group."""
        assert groups_ids is None or isinstance(groups_ids, list)

        query = db.session.query(
            Group.id, func.count(GroupAdmin.id)
        ).join(
            GroupAdmin
        ).group_by(
            Group.id
        )

        if groups_ids:
            query = query.filter(Group.id.in_(groups_ids))

        return query