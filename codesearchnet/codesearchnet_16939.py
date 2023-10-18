def cornice_enable_openapi_explorer(
        config,
        api_explorer_path='/api-explorer',
        permission=NO_PERMISSION_REQUIRED,
        route_factory=None,
        **kwargs):
    """
    :param config:
        Pyramid configurator object
    :param api_explorer_path:
        where to expose Swagger UI interface view
    :param permission:
        pyramid permission for those views
    :param route_factory:
        factory for context object for those routes

    This registers and configures the view that serves api explorer
    """
    config.add_route('cornice_swagger.api_explorer_path', api_explorer_path,
                     factory=route_factory)
    config.add_view('cornice_swagger.views.swagger_ui_template_view',
                    permission=permission,
                    route_name='cornice_swagger.api_explorer_path')