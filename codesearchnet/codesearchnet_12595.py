def parse_query_by_json(data):
    """
    ['and',
        ['==', 't1', 'col1', val1],
        ['!=', 't1', 'col2', 't2', 'col2'],
        ['and',
            ['==', 't1', 'col3', val3],
            ['!=', 't2', 'col4', val4],
        ]
    ]
    :return:
    :param data: 
    :return: 
    """
    data = json.loads(data)

    for i in ('tables', 'columns', 'conditions'):
        if i not in data:
            raise QueryException("query: %s not found" % i)

    tables = data['tables']
    columns = data['columns']
    conditions = data['conditions']

    def parse_stmt(s, expr_cls, all_op, multi_items_op):
        if len(s) == 0:
            return []

        if s[0] in all_op:
            if s[0] in multi_items_op:
                values = []
                for i in s[1:]:
                    values.append(parse_stmt(i, expr_cls, all_op, multi_items_op))
                return expr_cls(None, s[0], None, values=values)
            else:
                if len(s) == 5:
                    # t1.c1 == t2.c2
                    lhs = Column(s[2], table=s[1])
                    rhs = Column(s[4], table=s[3])
                    if (s[1] not in tables) or (s[3] not in tables):
                        raise QueryException('Bad query')
                    return expr_cls(lhs, s[0], rhs)
                else:
                    # t1.c1 == val
                    lhs = Column(s[2], table=s[1])
                    if s[1] not in tables:
                        raise QueryException('Bad query')
                    return expr_cls(lhs, s[0], s[3])
        else:
            raise QueryException('Bad query')

    query_op = ('+', '-', '*', '/')
    query_columns = []

    for i in columns:
        if len(i) == 2:
            query_columns.append(Column(i[1], table=i[0]))
        else:
            query_columns.append(parse_stmt(i, QueryExpression, query_op, query_op))
    wheres = parse_stmt(conditions, ConditionExpression, _operator_map, ('and', 'or',))

    return {
        'tables': tables,
        'columns': query_columns,
        'wheres': wheres,
    }