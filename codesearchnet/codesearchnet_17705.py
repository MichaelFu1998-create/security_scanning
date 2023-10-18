def paginate_link_tag(item):
    """
    Create an A-HREF tag that points to another page usable in paginate.
    """
    a_tag = Page.default_link_tag(item)
    if item['type'] == 'current_page':
        return make_html_tag('li', a_tag, **{'class': 'blue white-text'})
    return make_html_tag('li', a_tag)