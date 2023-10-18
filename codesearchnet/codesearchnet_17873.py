def query_by_user(cls, user, with_pending=False, eager=False):
        """Query group by user.

        :param user: User object.
        :param bool with_pending: Whether to include pending users.
        :param bool eager: Eagerly fetch group members.
        :returns: Query object.
        """
        q1 = Group.query.join(Membership).filter_by(user_id=user.get_id())
        if not with_pending:
            q1 = q1.filter_by(state=MembershipState.ACTIVE)
        if eager:
            q1 = q1.options(joinedload(Group.members))

        q2 = Group.query.join(GroupAdmin).filter_by(
            admin_id=user.get_id(), admin_type=resolve_admin_type(user))
        if eager:
            q2 = q2.options(joinedload(Group.members))

        query = q1.union(q2).with_entities(Group.id)

        return Group.query.filter(Group.id.in_(query))