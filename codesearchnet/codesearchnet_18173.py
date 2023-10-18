def update_alias_mapping(settings, alias, new_mapping):
    """
    Override `alias` mapping in the user configuration file with the given `new_mapping`, which should be a tuple with
    2 or 3 elements (in the form `(project_id, activity_id, role_id)`).
    """
    mapping = aliases_database[alias]
    new_mapping = Mapping(mapping=new_mapping, backend=mapping.backend)
    aliases_database[alias] = new_mapping
    settings.add_alias(alias, new_mapping)
    settings.write_config()