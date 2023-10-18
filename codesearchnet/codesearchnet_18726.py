def strip_oembeds(text, args=None):
    """
    Take a block of text and strip all the embeds from it, optionally taking
    a maxwidth, maxheight / resource_type
    
    Usage:
    {{ post.content|strip_embeds }}
    
    {{ post.content|strip_embeds:"600x600xphoto" }}
    
    {{ post.content|strip_embeds:"video" }}
    """
    resource_type = width = height = None
    if args:
        dimensions = args.lower().split('x')
        if len(dimensions) in (3, 1):
            resource_type = dimensions.pop()

        if len(dimensions) == 2:
            width, height = map(lambda x: int(x), dimensions)
    
    client = OEmbedConsumer()
    return mark_safe(client.strip(text, width, height, resource_type))