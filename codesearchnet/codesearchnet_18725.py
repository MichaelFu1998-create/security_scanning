def extract_oembeds(text, args=None):
    """
    Extract oembed resources from a block of text.  Returns a list
    of dictionaries.

    Max width & height can be specified:
    {% for embed in block_of_text|extract_oembeds:"400x300" %}

    Resource type can be specified:
    {% for photo_embed in block_of_text|extract_oembeds:"photo" %}

    Or both:
    {% for embed in block_of_text|extract_oembeds:"400x300xphoto" %}
    """
    resource_type = width = height = None
    if args:
        dimensions = args.lower().split('x')
        if len(dimensions) in (3, 1):
            resource_type = dimensions.pop()

        if len(dimensions) == 2:
            width, height = map(lambda x: int(x), dimensions)

    client = OEmbedConsumer()
    return client.extract(text, width, height, resource_type)