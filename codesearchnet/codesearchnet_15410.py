def update_module_state(cursor, module_ident,
                        state_name, recipe):  # pragma: no cover
    """This updates the module's state in the database."""
    cursor.execute("""\
UPDATE modules
SET stateid = (
    SELECT stateid FROM modulestates WHERE statename = %s
), recipe = %s, baked = now() WHERE module_ident = %s""",
                   (state_name, recipe, module_ident))