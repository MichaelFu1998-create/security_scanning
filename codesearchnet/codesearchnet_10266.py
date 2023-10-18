def get_canonical_link(self):
        """
        if the article has meta canonical link set in the url
        """
        if self.article.final_url:
            kwargs = {'tag': 'link', 'attr': 'rel', 'value': 'canonical'}
            meta = self.parser.getElementsByTag(self.article.doc, **kwargs)
            if meta is not None and len(meta) > 0:
                href = self.parser.getAttribute(meta[0], 'href')
                if href:
                    href = href.strip()
                    o = urlparse(href)
                    if not o.hostname:
                        tmp = urlparse(self.article.final_url)
                        domain = '%s://%s' % (tmp.scheme, tmp.hostname)
                        href = urljoin(domain, href)
                    return href
        return self.article.final_url