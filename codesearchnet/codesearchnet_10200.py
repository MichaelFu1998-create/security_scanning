def get_data_view(self, data_view_id):
        """
        Retrieves a summary of information for a given data view
            - view id
            - name
            - description
            - columns

        :param data_view_id: The ID number of the data view to which the
            run belongs, as a string
        :type data_view_id: str
        """

        url = routes.get_data_view(data_view_id)

        response = self._get(url).json()

        result = response["data"]["data_view"]

        datasets_list = []
        for dataset in result["datasets"]:
            datasets_list.append(Dataset(
                name=dataset["name"],
                id=dataset["id"],
                description=dataset["description"]
            ))

        columns_list = []
        for column in result["columns"]:
            columns_list.append(ColumnFactory.from_dict(column))

        return DataView(
            view_id=data_view_id,
            name=result["name"],
            description=result["description"],
            datasets=datasets_list,
            columns=columns_list,
        )