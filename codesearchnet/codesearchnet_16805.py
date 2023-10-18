def create_blueprint(endpoints):
    """Create Invenio-Deposit-UI blueprint.

    See: :data:`invenio_deposit.config.DEPOSIT_RECORDS_UI_ENDPOINTS`.

    :param endpoints: List of endpoints configuration.
    :returns: The configured blueprint.
    """
    from invenio_records_ui.views import create_url_rule

    blueprint = Blueprint(
        'invenio_deposit_ui',
        __name__,
        static_folder='../static',
        template_folder='../templates',
        url_prefix='',
    )

    @blueprint.errorhandler(PIDDeletedError)
    def tombstone_errorhandler(error):
        """Render tombstone page."""
        return render_template(
            current_app.config['DEPOSIT_UI_TOMBSTONE_TEMPLATE'],
            pid=error.pid,
            record=error.record or {},
        ), 410

    for endpoint, options in (endpoints or {}).items():
        options = deepcopy(options)
        options.pop('jsonschema', None)
        options.pop('schemaform', None)
        blueprint.add_url_rule(**create_url_rule(endpoint, **options))

    @blueprint.route('/deposit')
    @login_required
    def index():
        """List user deposits."""
        return render_template(current_app.config['DEPOSIT_UI_INDEX_TEMPLATE'])

    @blueprint.route('/deposit/new')
    @login_required
    def new():
        """Create new deposit."""
        deposit_type = request.values.get('type')
        return render_template(
            current_app.config['DEPOSIT_UI_NEW_TEMPLATE'],
            record={'_deposit': {'id': None}},
            jsonschema=current_deposit.jsonschemas[deposit_type],
            schemaform=current_deposit.schemaforms[deposit_type],
        )

    return blueprint