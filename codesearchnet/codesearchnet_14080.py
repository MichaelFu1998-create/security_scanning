def morguefile(query, n=10, top=10):
    """
    Returns a list of colors drawn from a morgueFile image.

    With the Web library installed,
    downloads a thumbnail from morgueFile and retrieves pixel colors.
    """

    from web import morguefile
    images = morguefile.search(query)[:top]
    path = choice(images).download(thumbnail=True, wait=10)

    return ColorList(path, n, name=query)