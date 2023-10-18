def extract_dicommetadata(self, token, item_id):
        """
        Extract DICOM metadata from the given item

        :param token: A valid token for the user in question.
        :type token: string
        :param item_id: id of the item to be extracted
        :type item_id: int | long
        :return: the item revision DAO
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['item'] = item_id
        response = self.request('midas.dicomextractor.extract', parameters)
        return response