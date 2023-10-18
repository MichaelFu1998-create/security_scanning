def webhook(*args, **kwargs):
    """
    Decorator to mark plugin functions as entry points for web calls

    * route - web route to register, uses Flask syntax
    * method - GET/POST, defaults to POST
    """
    def wrapper(func):
        func.is_webhook = True
        func.route = args[0]
        func.form_params = kwargs.get('form_params', [])
        func.method = kwargs.get('method', 'POST')
        return func
    return wrapper