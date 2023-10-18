async def update(self, records: Iterable[DataRecord], values: SQLValuesToWrite, returning=False) -> Union[int, Iterable[DataRecord]]:
        """
        :param records:
        :param values:
        :param returning:
        :return: return count if returning is False, otherwise records
        """
        raise NotImplementedError()