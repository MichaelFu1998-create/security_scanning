def app_class():
    """Create Flask application class.

    Invenio-Files-REST needs to patch the Werkzeug form parsing in order to
    support streaming large file uploads. This is done by subclassing the Flask
    application class.
    """
    try:
        pkg_resources.get_distribution('invenio-files-rest')
        from invenio_files_rest.app import Flask as FlaskBase
    except pkg_resources.DistributionNotFound:
        from flask import Flask as FlaskBase

    # Add Host header validation via APP_ALLOWED_HOSTS configuration variable.
    class Request(TrustedHostsMixin, FlaskBase.request_class):
        pass

    class Flask(FlaskBase):
        request_class = Request

    return Flask