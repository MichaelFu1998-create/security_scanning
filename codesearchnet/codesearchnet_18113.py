def manage(group_id):
    """Manage your group."""
    group = Group.query.get_or_404(group_id)
    form = GroupForm(request.form, obj=group)

    if form.validate_on_submit():
        if group.can_edit(current_user):
            try:
                group.update(**form.data)
                flash(_('Group "%(name)s" was updated', name=group.name),
                      'success')
            except Exception as e:
                flash(str(e), 'error')
                return render_template(
                    "invenio_groups/new.html",
                    form=form,
                    group=group,
                )
        else:
            flash(
                _(
                    'You cannot edit group %(group_name)s',
                    group_name=group.name
                ),
                'error'
            )

    return render_template(
        "invenio_groups/new.html",
        form=form,
        group=group,
    )