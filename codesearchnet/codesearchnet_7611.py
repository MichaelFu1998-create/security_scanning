def _get_link(self, cobj):
        """Get a valid link, False if not found"""

        fname_idx = None
        full_name = cobj['module_short'] + '.' + cobj['name']
        if full_name in self._searchindex['objects']:
            value = self._searchindex['objects'][full_name]
            if isinstance(value, dict):
                value = value[next(iter(value.keys()))]
            fname_idx = value[0]
        elif cobj['module_short'] in self._searchindex['objects']:
            value = self._searchindex['objects'][cobj['module_short']]
            if cobj['name'] in value.keys():
                fname_idx = value[cobj['name']][0]

        if fname_idx is not None:
            fname = self._searchindex['filenames'][fname_idx] + '.html'

            if self._is_windows:
                fname = fname.replace('/', '\\')
                link = os.path.join(self.doc_url, fname)
            else:
                link = posixpath.join(self.doc_url, fname)

            if hasattr(link, 'decode'):
                link = link.decode('utf-8', 'replace')

            if link in self._page_cache:
                html = self._page_cache[link]
            else:
                html = get_data(link, self.gallery_dir)
                self._page_cache[link] = html

            # test if cobj appears in page
            comb_names = [cobj['module_short'] + '.' + cobj['name']]
            if self.extra_modules_test is not None:
                for mod in self.extra_modules_test:
                    comb_names.append(mod + '.' + cobj['name'])
            url = False
            if hasattr(html, 'decode'):
                # Decode bytes under Python 3
                html = html.decode('utf-8', 'replace')

            for comb_name in comb_names:
                if hasattr(comb_name, 'decode'):
                    # Decode bytes under Python 3
                    comb_name = comb_name.decode('utf-8', 'replace')
                if comb_name in html:
                    url = link + u'#' + comb_name
            link = url
        else:
            link = False

        return link