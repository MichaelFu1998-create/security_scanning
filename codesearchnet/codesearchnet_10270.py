def __crawl(self, crawl_candidate):
        ''' wrap the crawling functionality '''
        def crawler_wrapper(parser, parsers_lst, crawl_candidate):
            try:
                crawler = Crawler(self.config, self.fetcher)
                article = crawler.crawl(crawl_candidate)
            except (UnicodeDecodeError, ValueError) as ex:
                if parsers_lst:
                    parser = parsers_lst.pop(0)  # remove it also!
                    return crawler_wrapper(parser, parsers_lst, crawl_candidate)
                else:
                    raise ex
            return article

        # use the wrapper
        parsers = list(self.config.available_parsers)
        parsers.remove(self.config.parser_class)
        return crawler_wrapper(self.config.parser_class, parsers, crawl_candidate)