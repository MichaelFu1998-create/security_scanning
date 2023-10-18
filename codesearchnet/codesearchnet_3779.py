def process_extra_vars(extra_vars_list, force_json=True):
    """Returns a string that is valid JSON or YAML and contains all the
    variables in every extra_vars_opt inside of extra_vars_list.

    Args:
       parse_kv (bool): whether to allow key=value syntax.
       force_json (bool): if True, always output json.
    """
    # Read from all the different sources and put into dictionary
    extra_vars = {}
    extra_vars_yaml = ""
    for extra_vars_opt in extra_vars_list:
        # Load file content if necessary
        if extra_vars_opt.startswith("@"):
            with open(extra_vars_opt[1:], 'r') as f:
                extra_vars_opt = f.read()
            # Convert text markup to a dictionary conservatively
            opt_dict = string_to_dict(extra_vars_opt, allow_kv=False)
        else:
            # Convert text markup to a dictionary liberally
            opt_dict = string_to_dict(extra_vars_opt, allow_kv=True)
        # Rolling YAML-based string combination
        if any(line.startswith("#") for line in extra_vars_opt.split('\n')):
            extra_vars_yaml += extra_vars_opt + "\n"
        elif extra_vars_opt != "":
            extra_vars_yaml += yaml.dump(
                opt_dict, default_flow_style=False) + "\n"
        # Combine dictionary with cumulative dictionary
        extra_vars.update(opt_dict)

    # Return contents in form of a string
    if not force_json:
        try:
            # Conditions to verify it is safe to return rolling YAML string
            try_dict = yaml.load(extra_vars_yaml, Loader=yaml.SafeLoader)
            assert type(try_dict) is dict
            debug.log('Using unprocessed YAML', header='decision', nl=2)
            return extra_vars_yaml.rstrip()
        except Exception:
            debug.log('Failed YAML parsing, defaulting to JSON',
                      header='decison', nl=2)
    if extra_vars == {}:
        return ""
    return json.dumps(extra_vars, ensure_ascii=False)