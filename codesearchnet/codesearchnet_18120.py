def new_member(group_id):
    """Add (invite) new member."""
    group = Group.query.get_or_404(group_id)

    if group.can_invite_others(current_user):
        form = NewMemberForm()

        if form.validate_on_submit():
            emails = filter(None, form.data['emails'].splitlines())
            group.invite_by_emails(emails)
            flash(_('Requests sent!'), 'success')
            return redirect(url_for('.members', group_id=group.id))

        return render_template(
            "invenio_groups/new_member.html",
            group=group,
            form=form
        )

    flash(
        _(
            'You cannot invite users or yourself (i.e. join) to the group '
            '%(group_name)s',
            group_name=group.name
        ),
        'error'
    )
    return redirect(url_for('.index'))