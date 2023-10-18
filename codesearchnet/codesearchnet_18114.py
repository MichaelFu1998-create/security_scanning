def delete(group_id):
    """Delete group."""
    group = Group.query.get_or_404(group_id)

    if group.can_edit(current_user):
        try:
            group.delete()
        except Exception as e:
            flash(str(e), "error")
            return redirect(url_for(".index"))

        flash(_('Successfully removed group "%(group_name)s"',
                group_name=group.name), 'success')
        return redirect(url_for(".index"))

    flash(
        _(
            'You cannot delete the group %(group_name)s',
            group_name=group.name
        ),
        'error'
    )
    return redirect(url_for(".index"))