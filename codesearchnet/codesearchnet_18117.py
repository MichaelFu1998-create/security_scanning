def approve(group_id, user_id):
    """Approve a user."""
    membership = Membership.query.get_or_404((user_id, group_id))
    group = membership.group

    if group.can_edit(current_user):
        try:
            membership.accept()
        except Exception as e:
            flash(str(e), 'error')
            return redirect(url_for('.requests', group_id=membership.group.id))

        flash(_('%(user)s accepted to %(name)s group.',
                user=membership.user.email,
                name=membership.group.name), 'success')
        return redirect(url_for('.requests', group_id=membership.group.id))

    flash(
        _(
            'You cannot approve memberships for the group %(group_name)s',
            group_name=group.name
        ),
        'error'
    )
    return redirect(url_for('.index'))