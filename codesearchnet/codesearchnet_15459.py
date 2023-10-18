def get_channel_image(self, channel, img_size=300, skip_cache=False):
        """Get the logo for a channel"""
        from bs4 import BeautifulSoup
        from wikipedia.exceptions import PageError
        import re
        import wikipedia
        wikipedia.set_lang('fr')

        if not channel:
            _LOGGER.error('Channel is not set. Could not retrieve image.')
            return

        # Check if the image is in cache
        if channel in self._cache_channel_img and not skip_cache:
            img = self._cache_channel_img[channel]
            _LOGGER.debug('Cache hit: %s -> %s', channel, img)
            return img

        channel_info = self.get_channel_info(channel)
        query = channel_info['wiki_page']
        if not query:
            _LOGGER.debug('Wiki page is not set for channel %s', channel)
            return
        _LOGGER.debug('Query: %s', query)
        # If there is a max image size defined use it.
        if 'max_img_size' in channel_info:
            if img_size > channel_info['max_img_size']:
                _LOGGER.info(
                    'Requested image size is bigger than the max, '
                    'setting it to %s', channel_info['max_img_size']
                )
                img_size = channel_info['max_img_size']
        try:
            page = wikipedia.page(query)
            _LOGGER.debug('Wikipedia article title: %s', page.title)
            soup = BeautifulSoup(page.html(), 'html.parser')
            images = soup.find_all('img')
            img_src = None
            for i in images:
                if i['alt'].startswith('Image illustrative'):
                    img_src = re.sub(r'\d+px', '{}px'.format(img_size),
                                     i['src'])
            img = 'https:{}'.format(img_src) if img_src else None
            # Cache result
            self._cache_channel_img[channel] = img
            return img
        except PageError:
            _LOGGER.error('Could not fetch channel image for %s', channel)