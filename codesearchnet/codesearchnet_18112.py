def new():
    """Create new group."""
    form = GroupForm(request.form)

    if form.validate_on_submit():
        try:
            group = Group.create(admins=[current_user], **form.data)

            flash(_('Group "%(name)s" created', name=group.name), 'success')
            return redirect(url_for(".index"))
        except IntegrityError:
            flash(_('Group creation failure'), 'error')

    return render_template(
        "invenio_groups/new.html",
        form=form,
    )