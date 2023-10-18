def accept(group_id):
    """Accpet pending invitation."""
    membership = Membership.query.get_or_404((current_user.get_id(), group_id))

    # no permission check, because they are checked during Memberships creating

    try:
        membership.accept()
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('.invitations', group_id=membership.group.id))

    flash(_('You are now part of %(name)s group.',
            user=membership.user.email,
            name=membership.group.name), 'success')
    return redirect(url_for('.invitations', group_id=membership.group.id))