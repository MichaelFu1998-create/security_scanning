def main():
    """
    Prints the complete YAML.

    """
    ep = requests.get(TRELLO_API_DOC).content
    root = html.fromstring(ep)

    links = root.xpath('//a[contains(@class, "reference internal")]/@href')
    pages = [requests.get(TRELLO_API_DOC + u)
             for u in links if u.endswith('index.html')]

    endpoints = []
    for page in pages:
        root = html.fromstring(page.content)
        sections = root.xpath('//div[@class="section"]/h2/..')
        for sec in sections:
            ep_html = etree.tostring(sec).decode('utf-8')
            ep_text = html2text(ep_html).splitlines()
            match = EP_DESC_REGEX.match(ep_text[0])
            if not match:
                continue
            ep_method, ep_url = match.groups()
            ep_text[0] = ' '.join([ep_method, ep_url])
            ep_doc = b64encode(gzip.compress('\n'.join(ep_text).encode('utf-8')))
            endpoints.append((ep_method, ep_url, ep_doc))

    print(yaml.dump(create_tree(endpoints)))