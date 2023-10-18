def query_requests(cls, admin, eager=False):
        """Get all pending group requests."""
        # Get direct pending request
        if hasattr(admin, 'is_superadmin') and admin.is_superadmin:
            q1 = GroupAdmin.query.with_entities(
                GroupAdmin.group_id)
        else:
            q1 = GroupAdmin.query_by_admin(admin).with_entities(
                GroupAdmin.group_id)
        q2 = Membership.query.filter(
            Membership.state == MembershipState.PENDING_ADMIN,
            Membership.id_group.in_(q1),
        )

        # Get request from admin groups your are member of
        q3 = Membership.query_by_user(
            user=admin, state=MembershipState.ACTIVE
        ).with_entities(Membership.id_group)
        q4 = GroupAdmin.query.filter(
            GroupAdmin.admin_type == 'Group', GroupAdmin.admin_id.in_(q3)
        ).with_entities(GroupAdmin.group_id)
        q5 = Membership.query.filter(
            Membership.state == MembershipState.PENDING_ADMIN,
            Membership.id_group.in_(q4))

        query = q2.union(q5)

        return query