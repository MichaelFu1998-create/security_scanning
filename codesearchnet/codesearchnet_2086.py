def setup(app):
    """When used for spinx extension."""
    global _is_sphinx
    _is_sphinx = True
    app.add_config_value('no_underscore_emphasis', False, 'env')
    app.add_source_parser('.md', M2RParser)
    app.add_directive('mdinclude', MdInclude)