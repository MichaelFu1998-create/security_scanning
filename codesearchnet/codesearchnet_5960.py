def rewrite_kwargs(conn_type, kwargs, module_name=None):
    """
    Manipulate connection keywords.
    
    Modifieds keywords based on connection type.

    There is an assumption here that the client has
    already been created and that these keywords are being
    passed into methods for interacting with various services.

    Current modifications:
    - if conn_type is not cloud and module is 'compute', 
      then rewrite project as name.
    - if conn_type is cloud and module is 'storage',
      then remove 'project' from dict.

    :param conn_type: E.g. 'cloud' or 'general'
    :type conn_type: ``str``

    :param kwargs: Dictionary of keywords sent in by user.
    :type kwargs: ``dict``

    :param module_name: Name of specific module that will be loaded.
                        Default is None.
    :type conn_type: ``str`` or None

    :returns kwargs with client and module specific changes
    :rtype: ``dict``
    """
    if conn_type != 'cloud' and module_name != 'compute':
        if 'project' in kwargs:
            kwargs['name'] = 'projects/%s' % kwargs.pop('project')
    if conn_type == 'cloud' and module_name == 'storage':
        if 'project' in kwargs:
            del kwargs['project']
    return kwargs