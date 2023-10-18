def parse_select(cls, text: str) -> Set:
        """
        get columns from select text
        :param text: col1, col2
        :return: ALL_COLUMNS or ['col1', 'col2']
        """
        if text == '*':
            return ALL_COLUMNS  # None means ALL
        selected_columns = set(filter(lambda x: x, map(str.strip, text.split(','))))
        if not selected_columns:
            raise InvalidParams("No column(s) selected")
        return selected_columns