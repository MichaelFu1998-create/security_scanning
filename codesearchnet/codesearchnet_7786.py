def _manage_args(parser,  args):
    """
    Checks and validate provided input
    """
    for item in data.CONFIGURABLE_OPTIONS:
        action = parser._option_string_actions[item]
        choices = default = ''
        input_value = getattr(args, action.dest)
        new_val = None
        # cannot count this until we find a way to test input
        if not args.noinput:  # pragma: no cover
            if action.choices:
                choices = ' (choices: {0})'.format(', '.join(action.choices))
            if input_value:
                if type(input_value) == list:
                    default = ' [default {0}]'.format(', '.join(input_value))
                else:
                    default = ' [default {0}]'.format(input_value)

            while not new_val:
                prompt = '{0}{1}{2}: '.format(action.help, choices, default)
                if action.choices in ('yes', 'no'):
                    new_val = utils.query_yes_no(prompt)
                else:
                    new_val = compat.input(prompt)
                new_val = compat.clean(new_val)
                if not new_val and input_value:
                    new_val = input_value
                if new_val and action.dest == 'templates':
                    if new_val != 'no' and not os.path.isdir(new_val):
                        sys.stdout.write('Given directory does not exists, retry\n')
                        new_val = False
                if new_val and action.dest == 'db':
                    action(parser, args, new_val, action.option_strings)
                    new_val = getattr(args, action.dest)
        else:
            if not input_value and action.required:
                raise ValueError(
                    'Option {0} is required when in no-input mode'.format(action.dest)
                )
            new_val = input_value
            if action.dest == 'db':
                action(parser, args, new_val, action.option_strings)
                new_val = getattr(args, action.dest)
        if action.dest == 'templates' and (new_val == 'no' or not os.path.isdir(new_val)):
            new_val = False
        if action.dest in ('bootstrap', 'starting_page'):
            new_val = (new_val == 'yes')
        setattr(args, action.dest, new_val)
    return args