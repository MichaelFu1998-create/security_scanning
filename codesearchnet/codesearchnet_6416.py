def yandex_metrica(parser, token):
    """
    Yandex.Metrica counter template tag.

    Renders Javascript code to track page visits. You must supply
    your website counter ID (as a string) in the
    ``YANDEX_METRICA_COUNTER_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return YandexMetricaNode()