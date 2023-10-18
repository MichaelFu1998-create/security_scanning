def includeme(config):
    """ The callable makes it possible to include rpcinterface
    in a Pyramid application.

    Calling ``config.include(twitcher.rpcinterface)`` will result in this
    callable being called.

    Arguments:

    * ``config``: the ``pyramid.config.Configurator`` object.
    """
    settings = config.registry.settings

    if asbool(settings.get('twitcher.rpcinterface', True)):
        LOGGER.debug('Twitcher XML-RPC Interface enabled.')

        # include twitcher config
        config.include('twitcher.config')

        # using basic auth
        config.include('twitcher.basicauth')

        # pyramid xml-rpc
        # http://docs.pylonsproject.org/projects/pyramid-rpc/en/latest/xmlrpc.html
        config.include('pyramid_rpc.xmlrpc')
        config.include('twitcher.db')
        config.add_xmlrpc_endpoint('api', '/RPC2')

        # register xmlrpc methods
        config.add_xmlrpc_method(RPCInterface, attr='generate_token', endpoint='api', method='generate_token')
        config.add_xmlrpc_method(RPCInterface, attr='revoke_token', endpoint='api', method='revoke_token')
        config.add_xmlrpc_method(RPCInterface, attr='revoke_all_tokens', endpoint='api', method='revoke_all_tokens')
        config.add_xmlrpc_method(RPCInterface, attr='register_service', endpoint='api', method='register_service')
        config.add_xmlrpc_method(RPCInterface, attr='unregister_service', endpoint='api', method='unregister_service')
        config.add_xmlrpc_method(RPCInterface, attr='get_service_by_name', endpoint='api', method='get_service_by_name')
        config.add_xmlrpc_method(RPCInterface, attr='get_service_by_url', endpoint='api', method='get_service_by_url')
        config.add_xmlrpc_method(RPCInterface, attr='clear_services', endpoint='api', method='clear_services')
        config.add_xmlrpc_method(RPCInterface, attr='list_services', endpoint='api', method='list_services')