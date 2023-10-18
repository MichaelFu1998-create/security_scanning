def _upsert_persons(cursor, person_ids, lookup_func):
    """Upsert's user info into the database.
    The model contains the user info as part of the role values.
    """
    person_ids = list(set(person_ids))  # cleanse data

    # Check for existing records to update.
    cursor.execute("SELECT personid from persons where personid = ANY (%s)",
                   (person_ids,))

    existing_person_ids = [x[0] for x in cursor.fetchall()]

    new_person_ids = [p for p in person_ids if p not in existing_person_ids]

    # Update existing records.
    for person_id in existing_person_ids:
        # TODO only update based on a delta against the 'updated' column.
        person_info = lookup_func(person_id)
        cursor.execute("""\
UPDATE persons
SET (personid, firstname, surname, fullname) =
    ( %(username)s, %(first_name)s, %(last_name)s,
     %(full_name)s)
WHERE personid = %(username)s""", person_info)

    # Insert new records.
    # Email is an empty string because
    # accounts no longer gives out user
    # email info but a string datatype
    # is still needed for legacy to
    # properly process the persons table
    for person_id in new_person_ids:
        person_info = lookup_func(person_id)
        cursor.execute("""\
INSERT INTO persons
(personid, firstname, surname, fullname, email)
VALUES
(%(username)s, %(first_name)s,
%(last_name)s, %(full_name)s, '')""", person_info)