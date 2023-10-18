def show_rules():
    """
    Show the list of available rules and quit
    :return:
    """
    from rules.loader import import_rules
    from rules.rule_list import all_rules
    rules = import_rules(all_rules)
    print("")
    for name, rule in rules.iteritems():
        heading = "{} (`{}`)".format(rule.description(), name)
        print("#### {} ####".format(heading))
        for line in rule.reason():
            print(line)
        print("")
    sys.exit(0)