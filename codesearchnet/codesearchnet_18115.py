def members(group_id):
    """List user group members."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    q = request.args.get('q', '')
    s = request.args.get('s', '')

    group = Group.query.get_or_404(group_id)
    if group.can_see_members(current_user):
        members = Membership.query_by_group(group_id, with_invitations=True)
        if q:
            members = Membership.search(members, q)
        if s:
            members = Membership.order(members, Membership.state, s)
        members = members.paginate(page, per_page=per_page)

        return render_template(
            "invenio_groups/members.html",
            group=group,
            members=members,
            page=page,
            per_page=per_page,
            q=q,
            s=s,
        )

    flash(
        _(
            'You are not allowed to see members of this group %(group_name)s.',
            group_name=group.name
        ),
        'error'
    )
    return redirect(url_for('.index'))