def parse_order(text):
        """
        :param text: order=id.desc, xxx.asc
        :return: [
            [<column>, asc|desc|default],
            [<column2>, asc|desc|default],
        ]
        """
        orders = []
        for i in map(str.strip, text.split(',')):
            items = i.split('.', 2)

            if len(items) == 1: column, order = items[0], 'default'
            elif len(items) == 2: column, order = items
            else: raise InvalidParams("Invalid order syntax")

            order = order.lower()
            if order not in ('asc', 'desc', 'default'):
                raise InvalidParams('Invalid order mode: %s' % order)

            if order != 'default':
                orders.append(SQLQueryOrder(column, order))
        return orders