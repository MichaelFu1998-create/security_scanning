def SimpleReflexAgentProgram(rules, interpret_input):
    "This agent takes action based solely on the percept. [Fig. 2.10]"
    def program(percept):
        state = interpret_input(percept)
        rule = rule_match(state, rules)
        action = rule.action
        return action
    return program