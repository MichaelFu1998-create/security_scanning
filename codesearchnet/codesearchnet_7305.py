def _conditional_links(assembled_specs, app_name):
    """ Given the assembled specs and app_name, this function will return all apps and services specified in
    'conditional_links' if they are specified in 'apps' or 'services' in assembled_specs. That means that
    some other part of the system has declared them as necessary, so they should be linked to this app """
    link_to_apps = []
    potential_links = assembled_specs['apps'][app_name]['conditional_links']
    for potential_link in potential_links['apps']:
        if potential_link in assembled_specs['apps']:
            link_to_apps.append(potential_link)
    for potential_link in potential_links['services']:
        if potential_link in assembled_specs['services']:
            link_to_apps.append(potential_link)
    return link_to_apps