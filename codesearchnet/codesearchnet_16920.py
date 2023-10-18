def open_api_json_view(request):
    """
    :param request:
    :return:

    Generates JSON representation of Swagger spec
    """
    doc = cornice_swagger.CorniceSwagger(
        cornice.service.get_services(), pyramid_registry=request.registry)
    kwargs = request.registry.settings['cornice_swagger.spec_kwargs']
    my_spec = doc.generate(**kwargs)
    return my_spec