def get_records(self, url):
        """
        Returns the records listed in the webpage given as
        parameter as a xml String.

        @param url: the url of the Journal, Book, Protocol or Reference work
        """
        page = urllib2.urlopen(url)
        pages = [BeautifulSoup(page)]
        #content spread over several pages?
        numpag = pages[0].body.findAll('span', attrs={'class': 'number-of-pages'})
        if len(numpag) > 0:
            if re.search('^\d+$', numpag[0].string):
                for i in range(int(numpag[0].string)-1):
                    page = urllib2.urlopen('%s/page/%i' % (url, i+2))
                    pages.append(BeautifulSoup(page))
            else:
                print("number of pages %s not an integer" % (numpag[0].string))
        impl = getDOMImplementation()
        doc = impl.createDocument(None, "collection", None)
        links = []
        for page in pages:
            links += page.body.findAll('p', attrs={'class': 'title'})
            links += page.body.findAll('h3', attrs={'class': 'title'})
        for link in links:
            record = self._get_record(link)
            doc.firstChild.appendChild(record)
        return doc.toprettyxml()