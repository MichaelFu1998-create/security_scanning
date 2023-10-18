def leave(group_id):
    """Leave group."""
    group = Group.query.get_or_404(group_id)

    if group.can_leave(current_user):
        try:
            group.remove_member(current_user)
        except Exception as e:
            flash(str(e), "error")
            return redirect(url_for('.index'))

        flash(
            _(
                'You have successfully left %(group_name)s group.',
                group_name=group.name
            ),
            'success'
        )
        return redirect(url_for('.index'))

    flash(
        _(
            'You cannot leave the group %(group_name)s',
            group_name=group.name
        ),
        'error'
    )
    return redirect(url_for('.index'))