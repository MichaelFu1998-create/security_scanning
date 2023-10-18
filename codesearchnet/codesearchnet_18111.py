def invitations():
    """List all user pending memberships."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    memberships = Membership.query_invitations(current_user, eager=True).all()

    return render_template(
        'invenio_groups/pending.html',
        memberships=memberships,
        page=page,
        per_page=per_page,
    )