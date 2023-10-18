def remove(group_id, user_id):
    """Remove user from a group."""
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(user_id)

    if group.can_edit(current_user):
        try:
            group.remove_member(user)
        except Exception as e:
            flash(str(e), "error")
            return redirect(urlparse(request.referrer).path)

        flash(_('User %(user_email)s was removed from %(group_name)s group.',
                user_email=user.email, group_name=group.name), 'success')
        return redirect(urlparse(request.referrer).path)

    flash(
        _(
            'You cannot delete users of the group %(group_name)s',
            group_name=group.name
        ),
        'error'
    )
    return redirect(url_for('.index'))