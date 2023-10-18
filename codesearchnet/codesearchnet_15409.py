def set_post_publications_state(cursor, module_ident, state_name,
                                state_message=''):  # pragma: no cover
    """This sets the post-publication state in the database."""
    cursor.execute("""\
INSERT INTO post_publications
  (module_ident, state, state_message)
  VALUES (%s, %s, %s)""", (module_ident, state_name, state_message))