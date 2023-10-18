def extract_json(fileobj, keywords, comment_tags, options):
    """
    Supports: gettext, ngettext. See package README or github ( https://github.com/tigrawap/pybabel-json ) for more usage info.
    """
    data=fileobj.read()
    json_extractor=JsonExtractor(data)
    strings_data=json_extractor.get_lines_data()

    for item in strings_data:
        messages = [item['content']]
        if item.get('funcname') == 'ngettext':
            messages.append(item['alt_content'])
        yield item['line_number'],item.get('funcname','gettext'),tuple(messages),[]