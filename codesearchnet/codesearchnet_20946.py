def init_app(self, app):
        """Flask application initialization."""
        state = _InvenioCSLRESTState(app)
        app.extensions['invenio-csl-rest'] = state
        return state