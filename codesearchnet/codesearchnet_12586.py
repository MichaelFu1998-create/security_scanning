async def insert(self, values_lst: Iterable[SQLValuesToWrite], returning=False) -> Union[int, List[DataRecord]]:
        """
        :param values_lst:
        :param returning:
        :return: return count if returning is False, otherwise records
        """
        raise NotImplementedError()