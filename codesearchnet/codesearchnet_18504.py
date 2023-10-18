def get_data_for_root(project_root):
    """This is the only API function of the projectfile module. It parses the Projectfiles
    from the given path and assembles the flattened command data structure.

    Returned data: {
        'min-version': (1, 0, 0),
        'description': 'Optional main description.',
        'commands': {
            'command_1': {
                'description': 'Optional command level description for command_1.',
                'script': [
                    'flattened',
                    'out command',
                    'list for',
                    'command_1',
                    ...
                ]
            }
            ...
        }
    }

    Raises:
        ProjectfileError with descriptive error message in the format of:
        {
            'path': 'Optional path for the corresponding Projectfile.',
            'line': 'Optional line number for the error in the Projectfile.',
            'error': 'Mandatory descriptive error message.'
        }


    :param project_root:
    :return: {dict} parsed and flattened commands with descriptions
    """
    raw_nodes = file_handler.get_node_list(project_root)
    command_tree = command_processor.generate_command_tree(raw_nodes)
    command_processor.flatten_commands(command_tree)
    command_processor.process_variables(command_tree)
    return command_tree