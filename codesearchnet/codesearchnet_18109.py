def index():
    """List all user memberships."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    q = request.args.get('q', '')

    groups = Group.query_by_user(current_user, eager=True)
    if q:
        groups = Group.search(groups, q)
    groups = groups.paginate(page, per_page=per_page)

    requests = Membership.query_requests(current_user).count()
    invitations = Membership.query_invitations(current_user).count()

    return render_template(
        'invenio_groups/index.html',
        groups=groups,
        requests=requests,
        invitations=invitations,
        page=page,
        per_page=per_page,
        q=q
    )