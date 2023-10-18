def get_price_text(price, request):
    """
    Return the localized converted price as string (ex. '$150 USD').

    If the local_currency switch is enabled and the users location has been determined this will convert the
    given price based on conversion rate from the Catalog service and return a localized string
    """
    if waffle.switch_is_active('local_currency') and get_localized_price_text:
        return get_localized_price_text(price, request)

    return format_price(price)