def requests():
    """List all pending memberships, listed only for group admins."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    memberships = Membership.query_requests(current_user, eager=True).all()

    return render_template(
        'invenio_groups/pending.html',
        memberships=memberships,
        requests=True,
        page=page,
        per_page=per_page,
    )