def add_common_check(self, actions, table, func):
        """
        emitted before query
        :param actions:
        :param table:
        :param func:
        :return:
        """
        self.common_checks.append([table, actions, func])

        """def func(ability, user, action, available_columns: list):
            pass
        """