def get_pif(self, dataset_id, uid, dataset_version = None):
        """
        Retrieves a PIF from a given dataset.

        :param dataset_id: The id of the dataset to retrieve PIF from
        :type dataset_id: int
        :param uid: The uid of the PIF to retrieve
        :type uid: str
        :param dataset_version: The dataset version to look for the PIF in. If nothing is supplied, the latest dataset version will be searched
        :type dataset_version: int
        :return: A :class:`Pif` object
        :rtype: :class:`Pif`
        """
        failure_message = "An error occurred retrieving PIF {}".format(uid)
        if dataset_version == None:
            response = self._get(routes.pif_dataset_uid(dataset_id, uid), failure_message=failure_message)
        else:
            response = self._get(routes.pif_dataset_version_uid(dataset_id, uid, dataset_version), failure_message=failure_message)

        return pif.loads(response.content.decode("utf-8"))