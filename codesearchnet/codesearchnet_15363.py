def declare_browsable_routes(config):
    """Declaration of routes that can be browsed by users."""
    # This makes our routes slashed, which is good browser behavior.
    config.add_notfound_view(default_exceptionresponse_view,
                             append_slash=True)

    add_route = config.add_route
    add_route('admin-index', '/a/')
    add_route('admin-moderation', '/a/moderation/')
    add_route('admin-api-keys', '/a/api-keys/')
    add_route('admin-add-site-messages', '/a/site-messages/',
              request_method='GET')
    add_route('admin-add-site-messages-POST', '/a/site-messages/',
              request_method='POST')
    add_route('admin-delete-site-messages', '/a/site-messages/',
              request_method='DELETE')
    add_route('admin-edit-site-message', '/a/site-messages/{id}/',
              request_method='GET')
    add_route('admin-edit-site-message-POST', '/a/site-messages/{id}/',
              request_method='POST')

    add_route('admin-content-status', '/a/content-status/')
    add_route('admin-content-status-single', '/a/content-status/{uuid}')

    add_route('admin-print-style', '/a/print-style/')
    add_route('admin-print-style-single', '/a/print-style/{style}')