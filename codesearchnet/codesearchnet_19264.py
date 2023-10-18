def compute_precedence(terminals, productions, precedence_levels):
        """Computes the precedence of terminal and production.

        The precedence of a terminal is it's level in the PRECEDENCE tuple. For
        a production, the precedence is the right-most terminal (if it exists).
        The default precedence is DEFAULT_PREC - (LEFT, 0).

        Returns:
            precedence - dict[terminal | production] = (assoc, level)

        """
        precedence = collections.OrderedDict()

        for terminal in terminals:
            precedence[terminal] = DEFAULT_PREC

        level_precs = range(len(precedence_levels), 0, -1)
        for i, level in zip(level_precs, precedence_levels):
            assoc = level[0]
            for symbol in level[1:]:
                precedence[symbol] = (assoc, i)

        for production, prec_symbol in productions:
            if prec_symbol is None:
                prod_terminals = [symbol for symbol in production.rhs
                                  if symbol in terminals] or [None]
                precedence[production] = precedence.get(prod_terminals[-1],
                                                        DEFAULT_PREC)
            else:
                precedence[production] = precedence.get(prec_symbol,
                                                        DEFAULT_PREC)

        return precedence