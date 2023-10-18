def KB_AgentProgram(KB):
    """A generic logical knowledge-based agent program. [Fig. 7.1]"""
    steps = itertools.count()

    def program(percept):
        t = steps.next()
        KB.tell(make_percept_sentence(percept, t))
        action = KB.ask(make_action_query(t))
        KB.tell(make_action_sentence(action, t))
        return action

    def make_percept_sentence(self, percept, t):
        return Expr("Percept")(percept, t)

    def make_action_query(self, t):
        return expr("ShouldDo(action, %d)" % t)

    def make_action_sentence(self, action, t):
        return Expr("Did")(action[expr('action')], t)

    return program