def read(self):
        """ Read the contents of the Annotation Resource

        :return: the contents of the resource
        :rtype: str or bytes or flask.response
        """
        if not self.__content__:
            self.__retriever__ = self.__resolver__.resolve(self.uri)
            self.__content__, self.__mimetype__ = self.__retriever__.read(self.uri)
        return self.__content__