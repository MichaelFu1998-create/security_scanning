def attachments(value, obj, width = WIDTH):
    """
    Parse the copy inside ``value`` and look for shortcodes in this format::
    
        <p>Here's an attachment</p>
        <p>[attachment 1]</p>
    
    Replace the shortcode with a full image, video or audio element, or download link
    
    :param obj: The object against which attachments are saved
    :param width: The width of images or audio/video tags (defaults to the ``ATTACHMENT_WIDTH`` SETTING)
    """
    
    match = ATTACHMENT_REGEX.search(value)
    safe = isinstance(value, (SafeString, SafeUnicode))
    
    while not match is None and match.end() <= len(value):
        start = match.start()
        end = match.end()
        groups = match.groups()
        
        if len(groups) > 0:
            index = groups[0]
            options = None
            
            if len(groups) > 1:
                options = groups[1]
                if options:
                    options = options.strip()
                    if options:
                        try:
                            options = split(smart_str(options))
                        except:
                            options = None
            
            args = []
            kwargs = {
                'width': width
            }
            
            if options:
                for option in options:
                    key, equals, val = option.partition('=')
                    if equals != '=':
                        if key and not val:
                            args.append(key)
                        continue
                    
                    kwargs[key] = val
            
            try:
                if isinstance(obj, dict):
                    inner = Attachment(
                        **obj['attachments__attachment'][int(index) - 1]
                    ).render(*args, **kwargs)
                else:
                    inner = obj.attachments.all()[int(index) - 1].render(*args, **kwargs)
            except:
                inner = ''
        else:
            inner = ''
        
        value = value[:start] + inner + value[end:]
        match = ATTACHMENT_REGEX.search(value, start + len(inner))
    
    if safe:
        return mark_safe(value)
    else:
        return value