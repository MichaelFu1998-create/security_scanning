def validate_specs_from_path(specs_path):
    """
    Validates Dusty specs at the given path. The following checks are performed:
        -That the given path exists
        -That there are bundles in the given path
        -That the fields in the specs match those allowed in our schemas
        -That references to apps, libs, and services point at defined specs
        -That there are no cycles in app and lib dependencies
    """
    # Validation of fields with schemer is now down implicitly through get_specs_from_path
    # We are dealing with Dusty_Specs class in this file
    log_to_client("Validating specs at path {}".format(specs_path))
    if not os.path.exists(specs_path):
        raise RuntimeError("Specs path not found: {}".format(specs_path))
    specs = get_specs_from_path(specs_path)
    _check_bare_minimum(specs)
    _validate_spec_names(specs)
    _validate_cycle_free(specs)
    log_to_client("Validation Complete!")