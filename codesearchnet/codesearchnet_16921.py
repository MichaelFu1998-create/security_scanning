def swagger_ui_script_template(request, **kwargs):
    """
    :param request:
    :return:

    Generates the <script> code that bootstraps Swagger UI, it will be injected
    into index template
    """
    swagger_spec_url = request.route_url('cornice_swagger.open_api_path')
    template = pkg_resources.resource_string(
        'cornice_swagger',
        'templates/index_script_template.html'
    ).decode('utf8')
    return Template(template).safe_substitute(
        swagger_spec_url=swagger_spec_url,
    )