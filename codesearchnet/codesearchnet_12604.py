def load():
    """
    Loads the built-in operators into the global test engine.
    """
    for operator in operators:
        module, symbols = operator[0], operator[1:]
        path = 'grappa.operators.{}'.format(module)

        # Dynamically import modules
        operator = __import__(path, None, None, symbols)

        # Register operators in the test engine
        for symbol in symbols:
            Engine.register(getattr(operator, symbol))