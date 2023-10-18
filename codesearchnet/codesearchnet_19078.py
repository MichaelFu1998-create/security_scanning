def get_codepoints():
        """ Return all XML <scanning-codepoints> in received XML """
        # response = requests.get(EXTENSIS_LANG_XML)
        # if response.status_code != 200:
        #     return []

        path = get_from_cache('languages.xml', EXTENSIS_LANG_XML)

        try:
            xml_content = open(path, 'r').read()
        except IOError:
            logging.error('Could not read languages.xml from cache')
            xml_content = ''

        content = re.sub('<!--.[^>]*-->', '', xml_content)
        doc = etree.fromstring(content.lstrip('`'))

        return doc.findall('.//scanning-codepoints')