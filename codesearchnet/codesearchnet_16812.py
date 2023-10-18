def create_blueprint(endpoints):
    """Create Invenio-Deposit-REST blueprint.

    See: :data:`invenio_deposit.config.DEPOSIT_REST_ENDPOINTS`.

    :param endpoints: List of endpoints configuration.
    :returns: The configured blueprint.
    """
    blueprint = Blueprint(
        'invenio_deposit_rest',
        __name__,
        url_prefix='',
    )
    create_error_handlers(blueprint)

    for endpoint, options in (endpoints or {}).items():
        options = deepcopy(options)

        if 'files_serializers' in options:
            files_serializers = options.get('files_serializers')
            files_serializers = {mime: obj_or_import_string(func)
                                 for mime, func in files_serializers.items()}
            del options['files_serializers']
        else:
            files_serializers = {}

        if 'record_serializers' in options:
            serializers = options.get('record_serializers')
            serializers = {mime: obj_or_import_string(func)
                           for mime, func in serializers.items()}
        else:
            serializers = {}

        file_list_route = options.pop(
            'file_list_route',
            '{0}/files'.format(options['item_route'])
        )
        file_item_route = options.pop(
            'file_item_route',
            '{0}/files/<path:key>'.format(options['item_route'])
        )

        options.setdefault('search_class', DepositSearch)
        search_class = obj_or_import_string(options['search_class'])

        # records rest endpoints will use the deposit class as record class
        options.setdefault('record_class', Deposit)
        record_class = obj_or_import_string(options['record_class'])

        # backward compatibility for indexer class
        options.setdefault('indexer_class', None)

        for rule in records_rest_url_rules(endpoint, **options):
            blueprint.add_url_rule(**rule)

        search_class_kwargs = {}
        if options.get('search_index'):
            search_class_kwargs['index'] = options['search_index']

        if options.get('search_type'):
            search_class_kwargs['doc_type'] = options['search_type']

        ctx = dict(
            read_permission_factory=obj_or_import_string(
                options.get('read_permission_factory_imp')
            ),
            create_permission_factory=obj_or_import_string(
                options.get('create_permission_factory_imp')
            ),
            update_permission_factory=obj_or_import_string(
                options.get('update_permission_factory_imp')
            ),
            delete_permission_factory=obj_or_import_string(
                options.get('delete_permission_factory_imp')
            ),
            record_class=record_class,
            search_class=partial(search_class, **search_class_kwargs),
            default_media_type=options.get('default_media_type'),
        )

        deposit_actions = DepositActionResource.as_view(
            DepositActionResource.view_name.format(endpoint),
            serializers=serializers,
            pid_type=options['pid_type'],
            ctx=ctx,
        )

        blueprint.add_url_rule(
            '{0}/actions/<any({1}):action>'.format(
                options['item_route'],
                ','.join(extract_actions_from_class(record_class)),
            ),
            view_func=deposit_actions,
            methods=['POST'],
        )

        deposit_files = DepositFilesResource.as_view(
            DepositFilesResource.view_name.format(endpoint),
            serializers=files_serializers,
            pid_type=options['pid_type'],
            ctx=ctx,
        )

        blueprint.add_url_rule(
            file_list_route,
            view_func=deposit_files,
            methods=['GET', 'POST', 'PUT'],
        )

        deposit_file = DepositFileResource.as_view(
            DepositFileResource.view_name.format(endpoint),
            serializers=files_serializers,
            pid_type=options['pid_type'],
            ctx=ctx,
        )

        blueprint.add_url_rule(
            file_item_route,
            view_func=deposit_file,
            methods=['GET', 'PUT', 'DELETE'],
        )
    return blueprint