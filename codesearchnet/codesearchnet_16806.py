def default_view_method(pid, record, template=None):
    """Default view method.

    Sends ``record_viewed`` signal and renders template.
    """
    record_viewed.send(
        current_app._get_current_object(),
        pid=pid,
        record=record,
    )

    deposit_type = request.values.get('type')

    return render_template(
        template,
        pid=pid,
        record=record,
        jsonschema=current_deposit.jsonschemas[deposit_type],
        schemaform=current_deposit.schemaforms[deposit_type],
    )