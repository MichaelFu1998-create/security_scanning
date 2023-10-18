def query_by_group(cls, group_or_id, with_invitations=False, **kwargs):
        """Get a group's members."""
        if isinstance(group_or_id, Group):
            id_group = group_or_id.id
        else:
            id_group = group_or_id

        if not with_invitations:
            return cls._filter(
                cls.query.filter_by(id_group=id_group),
                **kwargs
            )
        else:
            return cls.query.filter(
                Membership.id_group == id_group,
                db.or_(
                    Membership.state == MembershipState.PENDING_USER,
                    Membership.state == MembershipState.ACTIVE
                )
            )