def get_subparser(parser, command):
  '''
  Retrieve the given subparser from parser
  '''
  # pylint: disable=protected-access
  subparsers_actions = [action for action in parser._actions
                        if isinstance(action, argparse._SubParsersAction)]

  # there will probably only be one subparser_action,
  # but better save than sorry
  for subparsers_action in subparsers_actions:
    # get all subparsers
    for choice, subparser in subparsers_action.choices.items():
      if choice == command:
        return subparser
  return None