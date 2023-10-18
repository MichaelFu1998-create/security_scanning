def make_coins(self, collection, text, subreference="", lang=None):
        """ Creates a CoINS Title string from information

        :param collection: Collection to create coins from
        :param text: Text/Passage object
        :param subreference: Subreference
        :param lang: Locale information
        :return: Coins HTML title value
        """
        if lang is None:
            lang = self.__default_lang__
        return "url_ver=Z39.88-2004"\
                 "&ctx_ver=Z39.88-2004"\
                 "&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook"\
                 "&rft_id={cid}"\
                 "&rft.genre=bookitem"\
                 "&rft.btitle={title}"\
                 "&rft.edition={edition}"\
                 "&rft.au={author}"\
                 "&rft.atitle={pages}"\
                 "&rft.language={language}"\
                 "&rft.pages={pages}".format(
                    title=quote(str(text.get_title(lang))), author=quote(str(text.get_creator(lang))),
                    cid=url_for(".r_collection", objectId=collection.id, _external=True),
                    language=collection.lang, pages=quote(subreference), edition=quote(str(text.get_description(lang)))
                 )