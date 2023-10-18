def retrain(self, dataview_id):
        """
        Start a model retraining
        :param dataview_id: The ID of the views
        :return:
        """
        url = 'data_views/{}/retrain'.format(dataview_id)
        response = self._post_json(url, data={})
        if response.status_code != requests.codes.ok:
            raise RuntimeError('Retrain requested ' + str(response.status_code) + ' response: ' + str(response.message))
        return True