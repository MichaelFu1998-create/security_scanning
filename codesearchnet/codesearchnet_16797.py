def execute(helper, config, args):
    """
    Lists solution stacks
    """
    out("Available solution stacks")
    for stack in helper.list_available_solution_stacks():
        out("    "+str(stack))
    return 0