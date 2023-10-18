def cornice_enable_openapi_view(
        config,
        api_path='/api-explorer/swagger.json',
        permission=NO_PERMISSION_REQUIRED,
        route_factory=None, **kwargs):
    """
    :param config:
        Pyramid configurator object
    :param api_path:
        where to expose swagger JSON definition view
    :param permission:
        pyramid permission for those views
    :param route_factory:
        factory for context object for those routes
    :param kwargs:
        kwargs that will be passed to CorniceSwagger's `generate()`

    This registers and configures the view that serves api definitions
    """
    config.registry.settings['cornice_swagger.spec_kwargs'] = kwargs
    config.add_route('cornice_swagger.open_api_path', api_path,
                     factory=route_factory)
    config.add_view('cornice_swagger.views.open_api_json_view',
                    renderer='json', permission=permission,
                    route_name='cornice_swagger.open_api_path')