def run_the_target(G, target, settings):
    """
    Wrapper function that sends to commands in a target's 'formula'
    to run_commands()

    Args:
        The graph we are going to build
        The target to run
        The settings dictionary
    """
    sprint = settings["sprint"]
    sprint("Running target {}".format(target))
    the_formula = get_the_node_dict(G, target)["formula"]
    run_commands(the_formula, settings)