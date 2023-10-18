def swagger_ui_template_view(request):
    """
    Serves Swagger UI page, default Swagger UI config is used but you can
    override the callable that generates the `<script>` tag by setting
    `cornice_swagger.swagger_ui_script_generator` in pyramid config, it defaults
    to 'cornice_swagger.views:swagger_ui_script_template'

    :param request:
    :return:
    """
    script_generator = request.registry.settings.get(
        'cornice_swagger.swagger_ui_script_generator',
        'cornice_swagger.views:swagger_ui_script_template')
    package, callable = script_generator.split(':')
    imported_package = importlib.import_module(package)
    script_callable = getattr(imported_package, callable)
    template = pkg_resources.resource_string(
        'cornice_swagger', 'templates/index.html').decode('utf8')

    html = Template(template).safe_substitute(
        ui_css_url=ui_css_url,
        ui_js_bundle_url=ui_js_bundle_url,
        ui_js_standalone_url=ui_js_standalone_url,
        swagger_ui_script=script_callable(request),
    )
    return Response(html)