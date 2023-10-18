def DTAgentProgram(belief_state):
    "A decision-theoretic agent. [Fig. 13.1]"
    def program(percept):
        belief_state.observe(program.action, percept)
        program.action = argmax(belief_state.actions(),
                                belief_state.expected_outcome_utility)
        return program.action
    program.action = None
    return program