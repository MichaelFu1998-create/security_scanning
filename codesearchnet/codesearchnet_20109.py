def auto_constraints(self, component=None):
        """
        Use CLDF reference properties to implicitely create foreign key constraints.

        :param component: A Table object or `None`.
        """
        if not component:
            for table in self.tables:
                self.auto_constraints(table)
            return

        if not component.tableSchema.primaryKey:
            idcol = component.get_column(term_uri('id'))
            if idcol:
                component.tableSchema.primaryKey = [idcol.name]

        self._auto_foreign_keys(component)

        try:
            table_type = self.get_tabletype(component)
        except ValueError:
            # New component is not a known CLDF term, so cannot add components
            # automatically. TODO: We might me able to infer some based on
            # `xxxReference` column properties?
            return

        # auto-add foreign keys targetting the new component:
        for table in self.tables:
            self._auto_foreign_keys(table, component=component, table_type=table_type)