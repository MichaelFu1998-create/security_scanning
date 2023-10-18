def declare_api_routes(config):
    """Declaration of routing"""
    add_route = config.add_route
    add_route('get-content', '/contents/{ident_hash}')
    add_route('get-resource', '/resources/{hash}')

    # User actions API
    add_route('license-request', '/contents/{uuid}/licensors')
    add_route('roles-request', '/contents/{uuid}/roles')
    add_route('acl-request', '/contents/{uuid}/permissions')

    # Publishing API
    add_route('publications', '/publications')
    add_route('get-publication', '/publications/{id}')
    add_route('publication-license-acceptance',
              '/publications/{id}/license-acceptances/{uid}')
    add_route('publication-role-acceptance',
              '/publications/{id}/role-acceptances/{uid}')
    # TODO (8-May-12017) Remove because the term collate is being phased out.
    add_route('collate-content', '/contents/{ident_hash}/collate-content')
    add_route('bake-content', '/contents/{ident_hash}/baked')

    # Moderation routes
    add_route('moderation', '/moderations')
    add_route('moderate', '/moderations/{id}')
    add_route('moderation-rss', '/feeds/moderations.rss')

    # API Key routes
    add_route('api-keys', '/api-keys')
    add_route('api-key', '/api-keys/{id}')