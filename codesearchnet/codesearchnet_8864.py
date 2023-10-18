def dropHistoricalTable(apps, schema_editor):
    """
    Drops the historical sap_success_factors table named herein.
    """
    table_name = 'sap_success_factors_historicalsapsuccessfactorsenterprisecus80ad'
    if table_name in connection.introspection.table_names():
        migrations.DeleteModel(
            name=table_name,
        )