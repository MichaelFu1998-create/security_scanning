async def select_page(self, info: SQLQueryInfo, size=1, page=1) -> Tuple[Tuple[DataRecord, ...], int]:
        """
        Select from database
        :param info:
        :param size: -1 means infinite
        :param page:
        :param need_count: if True, get count as second return value, otherwise -1
        :return: records. count
        """
        raise NotImplementedError()