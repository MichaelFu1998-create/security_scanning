def bump_version(cursor, uuid, is_minor_bump=False):
    """Bump to the next version of the given content identified
    by ``uuid``. Returns the next available version as a version tuple,
    containing major and minor version.
    If ``is_minor_bump`` is ``True`` the version will minor bump. That is
    1.2 becomes 1.3 in the case of Collections. And 2 becomes 3 for
    Modules regardless of this option.
    """
    cursor.execute("""\
SELECT portal_type, major_version, minor_version
FROM latest_modules
WHERE uuid = %s::uuid""", (uuid,))
    type_, major_version, minor_version = cursor.fetchone()
    incr = 1
    if type_ == 'Collection' and is_minor_bump:
        minor_version = minor_version + incr
    else:
        major_version = major_version + incr
    return (major_version, minor_version,)