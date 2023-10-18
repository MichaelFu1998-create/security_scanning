def md_jdbc_virtual_table(key, node):
    """Extract metadata JDBC Virtual Tables from an xml node"""
    name = node.find("name")
    sql = node.find("sql")
    escapeSql = node.find("escapeSql")
    escapeSql = escapeSql.text if escapeSql is not None else None
    keyColumn = node.find("keyColumn")
    keyColumn = keyColumn.text if keyColumn is not None else None
    n_g = node.find("geometry")
    geometry = JDBCVirtualTableGeometry(n_g.find("name"), n_g.find("type"), n_g.find("srid"))
    parameters = []
    for n_p in node.findall("parameter"):
        p_name = n_p.find("name")
        p_defaultValue = n_p.find("defaultValue")
        p_defaultValue = p_defaultValue.text if p_defaultValue is not None else None
        p_regexpValidator = n_p.find("regexpValidator")
        p_regexpValidator = p_regexpValidator.text if p_regexpValidator is not None else None
        parameters.append(JDBCVirtualTableParam(p_name, p_defaultValue, p_regexpValidator))

    return JDBCVirtualTable(name, sql, escapeSql, geometry, keyColumn, parameters)