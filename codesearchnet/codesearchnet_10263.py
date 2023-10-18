def infos(self):
        ''' dict: The summation of all data available about the extracted article

            Note:
                Read only '''
        data = {
            "meta": {
                "description": self.meta_description,
                "lang": self.meta_lang,
                "keywords": self.meta_keywords,
                "favicon": self.meta_favicon,
                "canonical": self.canonical_link,
                "encoding": self.meta_encoding
            },
            "image": None,
            "domain": self.domain,
            "title": self.title,
            "cleaned_text": self.cleaned_text,
            "opengraph": self.opengraph,
            "tags": self.tags,
            "tweets": self.tweets,
            "movies": [],
            "links": self.links,
            "authors": self.authors,
            "publish_date": self.publish_date
        }

        # image
        if self.top_image is not None:
            data['image'] = {
                'url': self.top_image.src,
                'width': self.top_image.width,
                'height': self.top_image.height,
                'type': 'image'
            }

        # movies
        for movie in self.movies:
            data['movies'].append({
                'embed_type': movie.embed_type,
                'provider': movie.provider,
                'width': movie.width,
                'height': movie.height,
                'embed_code': movie.embed_code,
                'src': movie.src,
            })

        return data