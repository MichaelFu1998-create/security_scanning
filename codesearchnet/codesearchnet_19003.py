def parse_html(self, html):
        """
        Use BeautifulSoup to parse HTML / XML
        http://www.crummy.com/software/BeautifulSoup/bs4/doc/#specifying-the-parser-to-use
        """

        soup = BeautifulSoup(html, self.parser)

        title_tag = soup.find('title')
        self.result.title = title_tag.string if title_tag else None

        self.soup = soup

        return soup