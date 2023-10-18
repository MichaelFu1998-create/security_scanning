def _get_id_compartment(id):
    """extract the compartment from the id string"""
    bracket_search = _bracket_re.findall(id)
    if len(bracket_search) == 1:
        return bracket_search[0][1]
    underscore_search = _underscore_re.findall(id)
    if len(underscore_search) == 1:
        return underscore_search[0][1]
    return None