def extract(self, url=None, raw_html=None):
        ''' Extract the most likely article content from the html page

            Args:
                url (str): URL to pull and parse
                raw_html (str): String representation of the HTML page
            Returns:
                Article: Representation of the article contents \
                including other parsed and extracted metadata '''
        crawl_candidate = CrawlCandidate(self.config, url, raw_html)
        return self.__crawl(crawl_candidate)