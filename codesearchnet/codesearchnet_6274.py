def _update_optional(cobra_object, new_dict, optional_attribute_dict,
                     ordered_keys):
    """update new_dict with optional attributes from cobra_object"""
    for key in ordered_keys:
        default = optional_attribute_dict[key]
        value = getattr(cobra_object, key)
        if value is None or value == default:
            continue
        new_dict[key] = _fix_type(value)