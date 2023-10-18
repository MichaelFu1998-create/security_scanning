def _extract_data_from_origin_map(origin_mapped_data: Dict[str, Iterable[DataSourceType]]) \
            -> Iterable[DataSourceType]:
        """
        Extracts the data from a data origin map.
        :param origin_mapped_data: a map containing the origin of the data as the key string and the data as the value
        :return: the data contained within the map
        """
        data = []
        for _, data_item in origin_mapped_data.items():
            data.extend(data_item)
        return data