def clean_title(self, title):
        """Clean title with the use of og:site_name
        in this case try to get rid of site name
        and use TITLE_SPLITTERS to reformat title
        """
        # check if we have the site name in opengraph data
        if "site_name" in list(self.article.opengraph.keys()):
            site_name = self.article.opengraph['site_name']
            # remove the site name from title
            title = title.replace(site_name, '').strip()
        elif (self.article.schema and "publisher" in self.article.schema and
              "name" in self.article.schema["publisher"]):
            site_name = self.article.schema["publisher"]["name"]
            # remove the site name from title
            title = title.replace(site_name, '').strip()

        # try to remove the domain from url
        if self.article.domain:
            pattern = re.compile(self.article.domain, re.IGNORECASE)
            title = pattern.sub("", title).strip()

        # split the title in words
        # TechCrunch | my wonderfull article
        # my wonderfull article | TechCrunch
        title_words = title.split()

        # check if first letter is in TITLE_SPLITTERS
        # if so remove it
        if title_words and title_words[0] in TITLE_SPLITTERS:
            title_words.pop(0)

        # check for a title that is empty or consists of only a
        # title splitter to avoid a IndexError below
        if not title_words:
            return ""

        # check if last letter is in TITLE_SPLITTERS
        # if so remove it
        if title_words[-1] in TITLE_SPLITTERS:
            title_words.pop(-1)

        # rebuild the title
        title = " ".join(title_words).strip()

        return title