def set_config(new_config={}):
    """ Reset config options to defaults, and then update (optionally)
    with the provided dictionary of options. """
    # The default base configuration.
    flask_app.base_config = dict(working_directory='.',
                                 template='collapse-input',
                                 debug=False,
                                 port=None)
    update_config(new_config)