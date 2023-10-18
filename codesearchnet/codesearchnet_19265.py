def make_tables(grammar, precedence):
        """Generates the ACTION and GOTO tables for the grammar.

        Returns:
            action - dict[state][lookahead] = (action, ...)
            goto - dict[state][just_reduced] = new_state

        """
        ACTION = {}
        GOTO = {}

        labels = {}

        def get_label(closure):
            if closure not in labels:
                labels[closure] = len(labels)
            return labels[closure]

        def resolve_shift_reduce(lookahead, s_action, r_action):
            s_assoc, s_level = precedence[lookahead]
            r_assoc, r_level = precedence[r_action[1]]

            if s_level < r_level:
                return r_action
            elif s_level == r_level and r_assoc == LEFT:
                return r_action
            else:
                return s_action

        initial, closures, goto = grammar.closures()
        for closure in closures:
            label = get_label(closure)

            for rule in closure:
                new_action, lookahead = None, rule.lookahead

                if not rule.at_end:
                    symbol = rule.rhs[rule.pos]
                    is_terminal = symbol in grammar.terminals
                    has_goto = symbol in goto[closure]
                    if is_terminal and has_goto:
                        next_state = get_label(goto[closure][symbol])
                        new_action, lookahead = ('shift', next_state), symbol
                elif rule.production == grammar.start and rule.at_end:
                    new_action = ('accept',)
                elif rule.at_end:
                    new_action = ('reduce', rule.production)

                if new_action is None:
                    continue

                prev_action = ACTION.get((label, lookahead))
                if prev_action is None or prev_action == new_action:
                    ACTION[label, lookahead] = new_action
                else:
                    types = (prev_action[0], new_action[0])
                    if types == ('shift', 'reduce'):
                        chosen = resolve_shift_reduce(lookahead,
                                                      prev_action,
                                                      new_action)
                    elif types == ('reduce', 'shift'):
                        chosen = resolve_shift_reduce(lookahead,
                                                      new_action,
                                                      prev_action)
                    else:
                        raise TableConflictError(prev_action, new_action)

                    ACTION[label, lookahead] = chosen

            for symbol in grammar.nonterminals:
                if symbol in goto[closure]:
                    GOTO[label, symbol] = get_label(goto[closure][symbol])

        return get_label(initial), ACTION, GOTO