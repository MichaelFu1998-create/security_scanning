def register(
        app):
    """
    Register all HTTP error code error handlers

    Currently, errors are handled by the JSON error handler.
    """

    # Pick a handler based on the requested format. Currently we assume the
    # caller wants JSON.
    error_handler = json.http_exception_error_handler


    @app.errorhandler(400)
    def handle_bad_request(
            exception):
        return error_handler(exception)


    @app.errorhandler(404)
    def handle_not_found(
            exception):
        return error_handler(exception)


    @app.errorhandler(405)
    def handle_method_not_allowed(
            exception):
        return error_handler(exception)


    @app.errorhandler(422)
    def handle_unprocessable_entity(
            exception):
        return error_handler(exception)


    @app.errorhandler(500)
    def handle_internal_server_error(
            exception):
        return error_handler(exception)