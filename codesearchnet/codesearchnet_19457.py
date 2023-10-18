def ModelBasedReflexAgentProgram(rules, update_state):
    "This agent takes action based on the percept and state. [Fig. 2.12]"
    def program(percept):
        program.state = update_state(program.state, program.action, percept)
        rule = rule_match(program.state, rules)
        action = rule.action
        return action
    program.state = program.action = None
    return program