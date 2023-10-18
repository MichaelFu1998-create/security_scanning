def _upsert_users(cursor, user_ids, lookup_func):
    """Upsert's user info into the database.
    The model contains the user info as part of the role values.
    """
    user_ids = list(set(user_ids))  # cleanse data

    # Check for existing records to update.
    cursor.execute("SELECT username from users where username = ANY (%s)",
                   (user_ids,))

    existing_user_ids = [x[0] for x in cursor.fetchall()]

    new_user_ids = [u for u in user_ids if u not in existing_user_ids]

    # Update existing records.
    for user_id in existing_user_ids:
        # TODO only update based on a delta against the 'updated' column.
        user_info = lookup_func(user_id)
        cursor.execute("""\
UPDATE users
SET (updated, username, first_name, last_name, full_name, title) =
    (CURRENT_TIMESTAMP, %(username)s, %(first_name)s, %(last_name)s,
     %(full_name)s, %(title)s)
WHERE username = %(username)s""", user_info)

    # Insert new records.
    for user_id in new_user_ids:
        user_info = lookup_func(user_id)
        cursor.execute("""\
INSERT INTO users
(username, first_name, last_name, full_name, suffix, title)
VALUES
(%(username)s, %(first_name)s, %(last_name)s, %(full_name)s,
 %(suffix)s, %(title)s)""", user_info)