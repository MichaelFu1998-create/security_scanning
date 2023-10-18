def get_catalog_admin_url_template(mode='change'):
    """
    Get template of catalog admin url.

    URL template will contain a placeholder '{catalog_id}' for catalog id.
    Arguments:
        mode e.g. change/add.

    Returns:
        A string containing template for catalog url.

    Example:
        >>> get_catalog_admin_url_template('change')
        "http://localhost:18381/admin/catalogs/catalog/{catalog_id}/change/"

    """
    api_base_url = getattr(settings, "COURSE_CATALOG_API_URL", "")

    # Extract FQDN (Fully Qualified Domain Name) from API URL.
    match = re.match(r"^(?P<fqdn>(?:https?://)?[^/]+)", api_base_url)

    if not match:
        return ""

    # Return matched FQDN from catalog api url appended with catalog admin path
    if mode == 'change':
        return match.group("fqdn").rstrip("/") + "/admin/catalogs/catalog/{catalog_id}/change/"
    elif mode == 'add':
        return match.group("fqdn").rstrip("/") + "/admin/catalogs/catalog/add/"