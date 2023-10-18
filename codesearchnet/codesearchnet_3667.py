def migrate(self, expression, name_migration_map=None):
        """ Migrate an expression created for a different constraint set to self.
            Returns an expression that can be used with this constraintSet

            All the foreign variables used in the expression are replaced by
            variables of this constraint set. If the variable was replaced before
            the replacement is taken from the provided migration map.

            The migration mapping is updated with new replacements.

            :param expression: the potentially foreign expression
            :param name_migration_map: mapping of already migrated variables. maps from string name of foreign variable to its currently existing migrated string name. this is updated during this migration.
            :return: a migrated expression where all the variables are local. name_migration_map is updated

        """
        if name_migration_map is None:
            name_migration_map = {}

        #  name_migration_map -> object_migration_map
        #  Based on the name mapping in name_migration_map build an object to
        #  object mapping to be used in the replacing of variables
        #  inv: object_migration_map's keys should ALWAYS be external/foreign
        #  expressions, and its values should ALWAYS be internal/local expressions
        object_migration_map = {}

        #List of foreign vars used in expression
        foreign_vars = itertools.filterfalse(self.is_declared, get_variables(expression))
        for foreign_var in foreign_vars:
            # If a variable with the same name was previously migrated
            if foreign_var.name in name_migration_map:
                migrated_name = name_migration_map[foreign_var.name]
                native_var = self.get_variable(migrated_name)
                assert native_var is not None, "name_migration_map contains a variable that does not exist in this ConstraintSet"
                object_migration_map[foreign_var] = native_var
            else:
                # foreign_var was not found in the local declared variables nor
                # any variable with the same name was previously migrated
                # let's make a new unique internal name for it
                migrated_name = foreign_var.name
                if migrated_name in self._declarations:
                    migrated_name = self._make_unique_name(f'{foreign_var.name}_migrated')
                # Create and declare a new variable of given type
                if isinstance(foreign_var, Bool):
                    new_var = self.new_bool(name=migrated_name)
                elif isinstance(foreign_var, BitVec):
                    new_var = self.new_bitvec(foreign_var.size, name=migrated_name)
                elif isinstance(foreign_var, Array):
                    # Note that we are discarding the ArrayProxy encapsulation
                    new_var = self.new_array(index_max=foreign_var.index_max, index_bits=foreign_var.index_bits, value_bits=foreign_var.value_bits, name=migrated_name).array
                else:
                    raise NotImplemented(f"Unknown expression type {type(var)} encountered during expression migration")
                # Update the var to var mapping
                object_migration_map[foreign_var] = new_var
                # Update the name to name mapping
                name_migration_map[foreign_var.name] = new_var.name

        #  Actually replace each appearance of migrated variables by the new ones
        migrated_expression = replace(expression, object_migration_map)
        return migrated_expression