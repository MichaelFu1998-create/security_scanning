def execute(helper, config, args):
    """
    Describes recent events for an environment.
    """
    environment_name = args.environment

    (events, next_token) = helper.describe_events(environment_name, start_time=datetime.now().isoformat())

    # swap C-Names
    for event in events:
        print(("["+event['Severity']+"] "+event['Message']))